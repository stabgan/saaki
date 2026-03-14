# �� Saaki — SA-AKI Mortality Prediction

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MIMIC-IV v3.1](https://img.shields.io/badge/data-MIMIC--IV%20v3.1-blue.svg)](https://physionet.org/content/mimiciv/)

Predicting in-hospital mortality for ICU patients with **Sepsis-Associated Acute Kidney Injury (SA-AKI)** using machine learning and survival analysis on the [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/) clinical database.

---

## Why This Matters

SA-AKI is one of the most lethal complications in critical care — sepsis patients who develop acute kidney injury face significantly elevated mortality risk. Early identification of high-risk patients can guide timely interventions such as renal-replacement therapy, vasopressor optimization, and fluid management.

This project builds predictive models from **356 clinical features** extracted from the first 24 hours of ICU stay, covering:

- **Vital signs** — heart rate, blood pressure, SpO₂, temperature, respiratory rate
- **Laboratory panels** — creatinine, lactate, bilirubin, CBC, coagulation, arterial blood gas
- **Severity scores** — APACHE III, SOFA (6 organ-specific components)
- **Comorbidities** — 17 Charlson comorbidity flags
- **Therapies** — mechanical ventilation, vasopressors, renal-replacement therapy
- **Fluid balance & urine output**

Each time-series feature includes 9 statistical aggregations (first, last, median, IQR, range, delta, AUC, slope, count) over the 24-hour window.

---

## Model Performance

| Model | AUROC | Notes |
|---|---|---|
| **CatBoost** | **0.794** | Best performer — native categorical handling |
| XGBoost | ~0.80 | Competitive with CatBoost |
| LightGBM | ~0.80 | Fastest training time |
| Logistic Regression | ~0.75 | Linear baseline (3-fold CV) |

**Targets:** AUROC ≥ 0.82 · Brier score ≤ 0.06 · C-index ≥ 0.82

---

## Quick Start

```bash
git clone https://github.com/stabgan/saaki.git
cd saaki
pip install -r requirements.txt
python saaki_model.py
```

The script runs logistic regression (cross-validated) followed by CatBoost training and reports AUROC on a stratified 80/20 test split.

> **Note:** You need the MIMIC-IV dataset placed in `data/` — see [Dataset](#dataset) below.

---

## Project Structure

```
saaki/
├── saaki_model.py               # Main training & evaluation pipeline
├── data/                        # MIMIC-IV SA-AKI cohort (requires PhysioNet access)
│   ├── mimic_saaki_final.csv
│   └── mimic_saaki_final.xlsx
├── doc/                         # Data dictionary (356 columns documented)
│   └── mimic_saaki_final_data_dictionary.md
├── catboost_info/               # CatBoost training logs
├── AGENTS.md                    # Full project context & methodology
├── plan.md                      # Roadmap & next steps
├── changelog.md                 # Version history
└── requirements.txt             # Python dependencies
```

---

## Tech Stack

| Category | Libraries |
|---|---|
| **ML Models** | CatBoost, XGBoost, LightGBM, scikit-learn |
| **Survival Analysis** | lifelines, scikit-survival |
| **Data Processing** | pandas, NumPy, SciPy |
| **Explainability** | SHAP, LIME |
| **Optimization** | Optuna, Hyperopt |
| **Visualization** | matplotlib, seaborn, Plotly |

---

## Methodology

**Binary classification** — `event_observed` (1 = in-hospital death, 0 = survived/censored)
**Survival analysis** — `time_to_event_hrs` with right-censoring

Pipeline:
1. Drop features with >99% missing values
2. Categorical encoding (CatBoost native / OneHot for sklearn pipelines)
3. Median imputation for numeric features
4. Stratified train/test split (80/20, seed=42)
5. Cross-validated AUROC evaluation

---

## Dataset

This project uses the [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/) database, which requires **credentialed access** through [PhysioNet](https://physionet.org/). You must:

1. Complete CITI training for human research data
2. Sign the MIMIC-IV data use agreement
3. Download and place the processed cohort file in `data/`

The data files are **not included** in this repository.

---

## Roadmap

- [ ] Feature engineering — missingness indicators, interaction terms
- [ ] Ensemble stacking — CatBoost + LightGBM + XGBoost
- [ ] Survival models — Cox PH (elastic-net), DeepSurv, AFT
- [ ] SHAP-based feature importance & clinical interpretability
- [ ] Fairness audits — AUROC parity across gender/ethnicity (Δ ≤ 0.05)
- [ ] Calibration analysis — Brier score, reliability diagrams
- [ ] Decision-curve analysis for net clinical benefit

---

## Known Issues

- **ID columns not dropped:** `stay_id`, `subject_id`, and `hadm_id` are retained as features during training — these should be excluded to avoid data leakage.
- **NaN handling in categoricals:** `.astype(str)` converts `NaN` to the string `'nan'` before `.fillna()` can act — missing categoricals are encoded as literal `'nan'` rather than `'NA'`.
- **Dependency bloat:** `requirements.txt` includes packages not yet used in the current pipeline (PyTorch, TensorFlow, etc.) and some deprecated packages (`pandas-profiling` → `ydata-profiling`, `pickle5` built into Python 3.10+).

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Author

Built by [Kaustabh Ganguly](https://github.com/stabgan) ([@stabgan](https://github.com/stabgan))
