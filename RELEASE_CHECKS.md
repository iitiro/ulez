# Release verification

- 8 regression tests passed.
- Full notebook executed with 5,000 trips and seed 42, producing 27 summaries and 135,000 per-scenario trip rows.
- Tests cover midnight crossings, distance preservation, restriction boundaries, category exclusivity, cancellation accounting, baseline isolation, and repeatability with a fixed seed.
- Sample generated figures were visually inspected.
- Coefficient provenance, physical emission units, city calibration, and empirical policy effects were not independently validated. Output labels and README state this limitation.

## Verification environment

Checked locally on 2026-11-20 with Python 3.14.2 on macOS. Runtime and test dependency versions are recorded in `constraints.txt`. Dependency resolution was also checked for the SPPACEU requirements targeting Python 3.12; the GitHub Actions platform/version matrix has been configured but has not run as part of this local audit.

## Repeat the offline checks

```sh
python -m pip install -r requirements-dev.txt -c constraints.txt
python -m pytest -q
```

No paid API calls were made. Tests use synthetic data and mocked service responses where external inputs are required. No Git commit, release tag, push, or GitHub Release was created by this preparation.
