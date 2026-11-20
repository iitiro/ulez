# ULEZ — Urban Mobility and Emissions Simulation

An exploratory model of how low-emission-zone restrictions influence urban trips and emissions.

- Generates 5,000 synthetic trips with a fixed random seed.
- Compares 27 alternatives across three zone sizes and nine restriction rules.
- Models trips that proceed, are canceled, or depart after a delay.
- Corrects scenario accounting, preserves the baseline, and recalculates delayed travel over hourly speeds.
- Exports computed scenario summaries, individual trip outcomes, and figures.

**Interpretation:** Emissions are reported in model units. The inherited coefficient formula and vehicle proxies are not independently calibrated; results are exploratory scenarios rather than measurements of a specific city's policy.
