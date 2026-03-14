# 🏥 Saaki — SA-AKI Mortality Prediction

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MIMIC-IV](https://img.shields.io/badge/data-MIMIC--IV%20v3.1-green.svg)](https://physionet.org/content/mimiciv/)

Predicting in-hospital mortality for ICU patients with **Sepsis-Associated Acute Kidney Injury (SA-AKI)** using the MIMIC-IV v3.1 dataset.

## Overview

SA-AKI is a critical condition in ICU settings with high mortality rates. This project builds predictive models using 356 clinical features extracted from the first 24 hours of ICU stay, including:

- **Vital signs** — heart rate, blood pressure, SpO2, temperature, respiratory rate
- **Laboratory values** — creatinine, lactate, bilirubin, CBC, coagulation panels, etc.
- **Severity scores** — APACHE III, SOFA components
- **Comorbidities** — 17 Charlson comorbidity flags
- **Therapies** — mechanical ventilation, vasopressors, RRT
- **Fluid balance & urine output**

Each time-series feature includes 9 statistical aggregations (first, last, median, IQR, range, delta, AUC, slope, count) over the 24h window.

## Results

| Model | AUROC | Notes |
|-------|-------|-------|
| CatBoost | **0.794** | Best performing, handles categoricals natively |
| XGBoost | ~0.80 | Competitive with CatBoost |
| LightGBM | ~0.80 | Fast training |
| Logistic Regression | ~0.75 | Baseline linear model |

Target: AUROC ≥ 0.82 (ongoing feature engineering)

## Quick Start

```bash
git clone https://github.com/stabgan/saaki.git
cd saaki
pip install -r requirements.txt
python saaki_model.py
```

## Project Structure

```
saaki/
├── data/                    # MIMIC-IV SA-AKI cohort (not included, requires PhysioNet access)
│   ├── mimic_saaki_final.csv
│   └── mimic_saaki_final.xlsx
├── saaki_model.py           # Main model training & evaluation
├── AGENTS.md                # Data dictionary (356 columns documented)
├── plan.md                  # Roadmap & next steps
├── changelog.md             # Version history
└── requirements.txt         # Dependencies
```

## Methodology

**Binary classification:** `event_observed` (1 = in-hospital death, 0 = survived/censored)

**Survival analysis:** `time_to_event_hrs` with right-censoring

Pipeline:
1. Drop features with >99% missing values
2. Categorical encoding (CatBoost native / OneHot for sklearn)
3. Median imputation for numeric features
4. Stratified train/test split (80/20)
5. Cross-validated AUROC evaluation

## Roadmap

- [ ] Feature engineering (missingness indicators, interaction terms)
- [ ] Ensemble methods (stacking CatBoost + LightGBM + XGBoost)
- [ ] Survival models (Cox PH, DeepSurv)
- [ ] SHAP-based feature importance & clinical interpretability
- [ ] Fairness audits across gender/ethnicity (AUROC parity Δ ≤ 0.05)
- [ ] Calibration analysis (Brier score ≤ 0.06)

## Data Access

This project uses [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/), which requires credentialed access through PhysioNet. The data files are not included in this repository.

## License

MIT License — see [LICENSE](LICENSE) for details.
