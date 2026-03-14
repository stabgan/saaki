# 🩺 Saaki — SA-AKI Mortality Prediction

Predicting in-hospital mortality for ICU patients with Sepsis-Associated Acute Kidney Injury using MIMIC-IV.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MIMIC-IV v3.1](https://img.shields.io/badge/data-MIMIC--IV%20v3.1-blue.svg)](https://physionet.org/content/mimiciv/)

---

## What It Does

SA-AKI (Sepsis-Associated Acute Kidney Injury) is one of the deadliest complications in critical care. This project builds ML models to identify high-risk patients early, using **356 clinical features** extracted from the first 24 hours of ICU stay:

- Vital signs (HR, BP, SpO₂, temperature, respiratory rate)
- Laboratory panels (creatinine, lactate, bilirubin, CBC, coagulation, ABG)
- Severity scores (APACHE III, SOFA — 6 organ-specific components)
- Comorbidities (17 Charlson flags)
- Therapies (mechanical ventilation, vasopressors, RRT)
- Fluid balance & urine output

Each time-series feature includes 9 statistical aggregations (first, last, median, IQR, range, delta, AUC, slope, count) over the 24-hour window.

---

## Methodology

Binary classification on `event_observed` (1 = in-hospital death, 0 = survived/censored), with `time_to_event_hrs` available for future survival analysis.

Pipeline:
1. Drop ID columns (`stay_id`, `subject_id`, `hadm_id`) to prevent data leakage
2. Drop features with >99% missing values
3. Categorical encoding — CatBoost native handling / OneHot for sklearn pipelines
4. Median imputation for numeric features
5. Stratified train/test split (80/20, seed=42)
6. Cross-validated AUROC evaluation

---

## Results

| Model | AUROC | Notes |
|---|---|---|
| **CatBoost** | **0.794** | Best performer — native categorical handling |
| XGBoost | ~0.80 | Competitive with CatBoost |
| LightGBM | ~0.80 | Fastest training time |
| Logistic Regression | ~0.75 | Linear baseline (3-fold CV) |

---

## Quick Start

```bash
git clone https://github.com/stabgan/saaki.git
cd saaki
pip install -r requirements.txt
python saaki_model.py
```

Runs logistic regression (cross-validated) followed by CatBoost training, reports AUROC on a stratified 80/20 test split.

> **Note:** Requires the MIMIC-IV dataset in `data/`. See [Dataset](#dataset) below.

---

## Project Structure

```
saaki/
├── saaki_model.py          # Training & evaluation pipeline
├── data/                   # MIMIC-IV SA-AKI cohort (PhysioNet access required)
│   ├── mimic_saaki_final.csv
│   └── mimic_saaki_final.xlsx
├── doc/                    # Data dictionary (356 columns)
├── requirements.txt        # Python dependencies
├── AGENTS.md               # Project context & methodology
├── plan.md                 # Roadmap
└── changelog.md            # Version history
```

---

## 🛠 Tech Stack

| | Category | Tools |
|---|---|---|
| 🤖 | ML Models | CatBoost, XGBoost, LightGBM, scikit-learn |
| 📊 | Survival Analysis | lifelines, scikit-survival |
| 🧮 | Data Processing | pandas, NumPy, SciPy |
| 🔍 | Explainability | SHAP, LIME |
| ⚙️ | Optimization | Optuna |
| 📈 | Visualization | matplotlib, seaborn, Plotly |
| 🏥 | Clinical Data | MIMIC-IV v3.1 via PhysioNet |

---

## Dataset

Uses [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/), which requires credentialed access through [PhysioNet](https://physionet.org/):

1. Complete CITI training for human research data
2. Sign the MIMIC-IV data use agreement
3. Place the processed cohort file in `data/`

Data files are **not included** in this repository.

---

## ⚠️ Known Issues

- AUROC plateaus around 0.80 — feature engineering (missingness indicators, interaction terms) and ensemble stacking are planned
- `requirements.txt` includes libraries for planned future work (survival analysis, explainability) not yet used in the main pipeline
- Survival modelling (Cox PH, DeepSurv) not yet implemented

---

## License

MIT — see [LICENSE](LICENSE) for details.

## Author

Built by [Kaustabh Ganguly](https://github.com/stabgan)
