# Paint R&D Versioning App

> A data tool built by someone who spent years manually tracking formulation changes in spreadsheets — and got tired of it.

Streamlit application for versioning, comparing, and analyzing industrial paint formulations. Designed for R&D teams in coatings and chemical manufacturing where every batch change needs to be documented, calculated, and validated.

---

## The Problem This Solves

In industrial paint manufacturing, formulation changes are constant: a supplier switches resin grades, a pigment goes out of stock, a customer requests a different sheen level.

Every change must be tracked. Every new version must be compared to the previous one. And every formulation needs its key technical parameters calculated — PVC, solids content, pigment/resin ratio — before it can go into production.

**The old way:** scattered Excel files, manual calculations, no version history, no easy way to compare two formulations side by side.

**This app:** register, calculate, version, and compare — all in one place.

---

## Who This Is For

- R&D chemists in coatings, adhesives, or specialty chemicals
- Technical managers who need audit trails for formulation changes
- QC analysts validating batch-to-batch consistency
- Anyone who has ever asked "which version of this formula did we use in March?"

---

## Features

| Feature | Description |
|---|---|
| **New Formulation** | Register ingredients by category with amounts, units, and solids content |
| **Auto-calculated parameters** | PVC, total solids, resin solids, pigment solids, pigment/resin ratio — calculated on save |
| **Version history** | Browse all saved formulations with full parameter history |
| **Side-by-side comparison** | Diff any two versions — metadata and ingredients — in one view |
| **Input validation** | Warns on missing solids data, zero batch size, and incomplete fields before saving |

---

## Technical Parameters Calculated

```
Total batch amount (g)
├── Resin solids (g and %)
├── Pigment solids (g)
├── Total solids (g and %)
├── Pigment/Resin ratio
└── PVC — Pigment Volume Concentration (requires density input)
```

These are the standard parameters used in industrial coatings formulation. If you work in the industry, you know them. If you're a recruiter: they determine hiding power, sheen, durability, and cost of the final product.

---

## Why I Built This

I spent 7+ years as a Technical Manager and R&D lead in paint manufacturing. The pain point this app addresses is real — I lived it. Formulation versioning in most small and mid-size coatings companies happens in shared Excel files with names like `formula_v3_FINAL_revised2.xlsx`.

This project demonstrates that domain expertise from industrial roles can be directly encoded into data tools — solving real problems, not just analyzing generic datasets.

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/Halexoh/paint-rnd-app.git
cd paint-rnd-app

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The app runs locally on `http://localhost:8501`. No external database required — formulations are stored in a local SQLite file.

---

## Tech Stack

| Tool | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Web app interface |
| Pandas | Data handling and parameter calculations |
| SQLite | Local persistent storage for formulation history |

---

## Certifications

| Certification | Institution | Status |
|---|---|---|
| Mathematics for Machine Learning Specialization | Imperial College London / Coursera | ✅ Feb 2026 |
| SQL (Intermediate) | HackerRank | ✅ May 2026 |
| Microsoft Power BI Data Analyst (PL-300) | Microsoft | 🔄 In progress |
| Google Data Analytics Professional Certificate | Google / Coursera | 🔄 In progress |

---

## Author

**Haderson Alexander Osorio**
Data Analyst | Biological Engineer | Medellín, Colombia

8+ years in industrial environments — coatings, chemical distribution, applied research. I build data tools that solve the problems I've seen firsthand in production and R&D.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-alexanderosorioanalytics-blue)](https://www.linkedin.com/in/alexanderosorioanalytics/)
[![GitHub](https://img.shields.io/badge/GitHub-Halexoh-black)](https://github.com/Halexoh)

> Available for remote roles in Data Analytics and Data Science — LATAM, Europe, and global.
