# ULEZ Simulation

Model how low-emission zone size, vehicle restrictions, and departure delays affect simulated urban trips and NOx emissions.

## Model overview

An exploratory notebook for comparing low-emission-zone scenarios in a simplified urban setting. It generates 5,000 synthetic trips and combines trip geometry, hourly traffic patterns, vehicle categories, Euro emission classes, and restriction rules.

The analysis compares trips that proceed, are canceled, or are delayed until restrictions end, and estimates the resulting changes in NOx emissions.

## Repository contents

`ULEZ_final.ipynb` contains the input assumptions, simulation, scenario calculations, charts, and CSV exports. Vehicle-age assumptions include Slovak fleet figures defined inside the notebook.

## Getting started

```sh
python3 -m pip install jupyter pandas numpy matplotlib
jupyter notebook ULEZ_final.ipynb
```

Review the assumptions and output paths, then execute the cells in order. The notebook exports intermediate trip datasets and scenario summaries to CSV.

## Interpretation

Results describe synthetic scenarios in an abstract city geometry. They do not constitute a calibrated evaluation of London's ULEZ or another specific city's policy. Random sampling can change results between runs; review random-seed handling when comparing scenarios.

## License

[GNU GPL v3](LICENSE).
