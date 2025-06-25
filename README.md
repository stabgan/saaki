# Sepsis-Associated Acute Kidney Injury (SA-AKI) Mortality Prediction

This project aims to develop a robust machine learning pipeline to predict in-hospital mortality for patients with Sepsis-Associated Acute Kidney Injury (SA-AKI). The models are built using data from the MIMIC-IV critical care database.

## Project Structure

```
.
├── Changelog.md
├── GEMINI.md
├── plan.md
├── README.md
├── requirements.txt
├── .gemini/
├── .venv/
├── code/
│   └── eda.py
├── data/
│   ├── mimic_saaki_final.csv
│   └── mimic_saaki_final.xlsx
└── doc/
    ├── Mimic Saaki Final Data Dictionary.docx
    ├── Mimic Saaki Final Data Dictionary.pdf
    ├── mimic_saaki_final_data_dictionary.md
    └── SA_AKI_ML_Experiment_Log.md
```

## Getting Started

### Prerequisites

- Python 3.11
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/stabgan/saaki.git
    cd saaki
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Data

The dataset used for this project is `mimic_saaki_final.csv`, which contains 356 features for patients with SA-AKI. The data dictionary, which provides a detailed description of each feature, can be found in the `doc` directory.

## Project Plan

The project is divided into the following phases:

1.  **Exploratory Data Analysis (EDA):** Understand the data distributions, missing values, and correlations.
2.  **Feature Engineering & Preprocessing:** Prepare the data for modeling.
3.  **Model Building:** Implement and train various classification and survival models.
4.  **Model Evaluation & Interpretation:** Assess model performance and understand their predictions.
5.  **Reproducibility & Reporting:** Ensure the results are reproducible and document the findings.

A detailed project plan can be found in `plan.md`.

## Tests

Run the test suite with:
```bash
pytest
```

## Changelog

All changes to the project are documented in `Changelog.md`.
