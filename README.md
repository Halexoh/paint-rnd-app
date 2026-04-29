# Paint R&D Versioning App

Streamlit application for versioning and comparing industrial paint formulations. Built to support R&D teams in tracking formulation changes, calculating technical parameters, and comparing versions side by side.

---

## Context

In industrial paint manufacturing, formulation changes are frequent and must be tracked carefully. Small changes in resin solids, pigment ratios, or additive amounts can significantly impact product quality and cost. This app provides a structured workflow to register, consult, and compare formulation versions.

---

## Features

- New Formulation: register ingredients by category with amounts, units and solids content
- History: browse all saved formulations with calculated technical parameters
- Compare Versions: side-by-side diff of metadata and ingredients between any two versions
- Auto-calculated: total solids, resin solids, pigment solids, pigment/resin ratio, PVC
- Input validation: warns on missing solids data, zero batch size, incomplete fields

---

## Technical Parameters Calculated

- Total batch amount (g)
- Resin solids (g and %)
- Pigment solids (g)
- Total solids (g and %)
- Pigment/Resin ratio
- PVC - Pigment Volume Concentration (requires density data)

---

## How to Run



---

## Tech Stack

Python, Streamlit, Pandas, SQLite

---

## Author

Alexander Osorio - Data Scientist, Biological Engineer
Medellin, Colombia. Available for remote LATAM/Global roles.
LinkedIn: https://www.linkedin.com/in/alexanderosorioanalytics/
GitHub: https://github.com/Halexoh
