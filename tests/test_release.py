import math
import pandas as pd
import pytest
from simulation import evaluate_scenarios, travel_profile, trip_outcome


def test_travel_profile_preserves_distance_across_midnight():
    speeds = [10.0] * 24
    speeds[23] = 20
    result = travel_profile(35, 23, speeds, lambda speed: 2)
    assert result == {"distance_km": 35.0, "duration_minutes": 150.0, "emissions": 70.0}


@pytest.mark.parametrize("distance", [-1, float("nan"), float("inf")])
def test_invalid_distances_rejected(distance):
    with pytest.raises(ValueError):
        travel_profile(distance, 0, [10] * 24, lambda speed: 1)


def test_restriction_outcomes_and_hour_boundaries():
    assert trip_outcome(5, 1, 12, True, False) == ("proceed", 0)
    assert trip_outcome(1, 1, 12, True, False) == ("cancel", 0)
    assert trip_outcome(1, 2, 12, False, True) == ("proceed", 0)
    assert trip_outcome(1, 4, 18, False, False) == ("delay", 2)
    assert trip_outcome(1, 4, 19, False, False) == ("delay", 1)
    assert trip_outcome(1, 4, 20, False, False) == ("proceed", 0)
    assert trip_outcome(1, 7, 9, False, False) == ("delay", 2)


def test_scenario_isolation_and_exact_totals():
    frame = pd.DataFrame([
        {"distance_km": 10, "time2": 18, "euro_class": "Euro 6", "vehicle_category": "petrol", "Diesel": 0, "Lux": 1, "Area 1_case": 5, "Area 2_case": 1, "Area 3_case": 1},
        {"distance_km": 5, "time2": 12, "euro_class": "Euro 2", "vehicle_category": "diesel", "Diesel": 1, "Lux": 0, "Area 1_case": 1, "Area 2_case": 1, "Area 3_case": 1},
    ])
    original = frame.copy(deep=True)
    summary, detail, baseline = evaluate_scenarios(frame, [10] * 24, lambda *args: 1)
    pd.testing.assert_frame_equal(frame, original)
    assert baseline == [10, 5]
    assert len(summary) == 27 and len(detail) == 54
    assert summary.eval("proceed + cancel + delay").eq(2).all()
    assert summary.baseline_emissions.eq(15).all()
    assert summary.loc[summary.area.eq("Area 1") & summary.rule.eq(1), "scenario_emissions"].item() == 10
    assert summary.loc[summary.area.eq("Area 2") & summary.rule.eq(1), "scenario_emissions"].item() == 0
    assert detail.loc[detail.status.eq("cancel"), "scenario_emissions"].eq(0).all()
    assert detail.scenario_emissions.map(math.isfinite).all()


def test_notebook_executes_with_repeatable_sampling(monkeypatch, tmp_path):
    from notebook_helpers import ROOT, notebook_namespace
    monkeypatch.chdir(ROOT)
    monkeypatch.setenv("ULEZ_N_TRIPS", "30")
    monkeypatch.setenv("ULEZ_OUTPUT_DIR", str(tmp_path / "first"))
    first = notebook_namespace("ULEZ_final.ipynb")
    monkeypatch.setenv("ULEZ_OUTPUT_DIR", str(tmp_path / "second"))
    second = notebook_namespace("ULEZ_final.ipynb")
    pd.testing.assert_frame_equal(first["summary_df"], second["summary_df"])
    pd.testing.assert_frame_equal(first["trips_df"], second["trips_df"])
    assert len(pd.read_csv(tmp_path / "first" / "scenario_trips.csv")) == 30 * 27


def test_published_notebooks_are_clean_and_valid():
    import nbformat
    from notebook_helpers import ROOT
    for path in ROOT.glob("*.ipynb"):
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                assert not cell.outputs
                assert cell.execution_count is None
