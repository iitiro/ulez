# ULEZ Simulation

Model how low-emission zone size, vehicle restrictions, and departure delays affect simulated urban trips and NOx emissions.

## Model overview

The notebook uses a 20 × 20 abstract urban grid, hourly traffic assumptions, vehicle categories, and Euro emission classes. Vehicle-age inputs include Slovak fleet figures defined inside the notebook. Three zones cover 15%, 30%, and 40% of the modeled area.

The default run generates **5,000 trips with random seed 42** and evaluates **27 independent alternatives**: three zone sizes × nine restriction rules. Trips proceed unchanged, are canceled, or wait up to two hours for a restriction to end. The hourly restriction windows are documented inside the notebook.

## Setup

Python 3.12 or newer is recommended. Run these commands from the repository directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -c constraints.txt
```

On Windows, activate the environment with `.venv\Scripts\activate`.
`constraints.txt` records the dependency versions used for the local release checks.

## Run

```sh
jupyter lab ULEZ_final.ipynb
```

Run all cells in order. No external service, credentials, or separate source dataset is required. `simulation.py` must remain alongside the notebook.

CSV files and figures are saved under `outputs/`, including:

- `trips_baseline.csv` — the generated trip sample and baseline emissions.
- `scenario_summary.csv` — one row per alternative, with category counts and emission totals.
- `scenario_trips.csv` — individual trip outcomes for each scenario.
- `figure_*.png` — generated figures.

Optional environment variables: `ULEZ_N_TRIPS`, `ULEZ_SEED`, and `ULEZ_OUTPUT_DIR`. Restart the kernel and rerun from the first cell after changing them. `MAX_WAIT_HOURS` can be changed in the first code cell.

## Release corrections

The scenario calculation preserves baseline data, assigns every trip to exactly one outcome per alternative, recalculates delayed trips over consecutive hourly speeds, and avoids adding alternative zones together. Plots use computed counts rather than manually entered example numbers. Earlier saved totals are superseded by the corrected calculation.

## Interpretation

This is an exploratory simulation, not a calibrated evaluation of London's ULEZ or another specific city. The original coefficient expression and vehicle proxies are retained; their provenance and physical units have not been independently validated. Emission outputs are therefore labeled **model units**. Accounting checks confirm internal consistency, not empirical validity. The model does not estimate rerouting, congestion feedback, or restrictions encountered after departure.

## Offline checks

```sh
python -m pip install -r requirements-dev.txt -c constraints.txt
python -m pytest -q
```

The test suite does not require API credentials. GitHub Actions is configured to repeat these checks on Python 3.12, 3.13, and 3.14 after push.

## License

[GNU GPL v3](LICENSE).
