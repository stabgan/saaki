# MTech Thesis Project Plan: In-ICU Mortality Prediction in SA-AKI

This document outlines the plan for the data science and statistical modeling part of the project.

## Phase 1: Exploratory Data Analysis (EDA)

1.  **Load Data:** Load the `mimic_saaki_final.csv` dataset.
2.  **Descriptive Statistics:** Compute summary statistics for all variables (mean, median, std, etc.).
3.  **Data Visualization:**
    *   Create histograms and density plots for numerical features.
    *   Create bar plots for categorical features.
    *   Generate violin plots to visualize outcome-stratified distributions.
4.  **Missing Data Analysis:**
    *   Quantify the extent of missing data for each feature.
    *   Visualize missing data patterns.
    *   Test for Missing Completely At Random (MCAR) using Little's test.
5.  **Correlation Analysis:**
    *   Compute a correlation matrix for numerical features.
    *   Visualize the correlation matrix using a heatmap.
    *   Check for multicollinearity using Variance Inflation Factor (VIF).

## Phase 2: Feature Engineering & Preprocessing

1.  **Handle Missing Data:**
    *   Apply appropriate imputation techniques (e.g., mean, median, KNN, MICE).
2.  **Encode Categorical Variables:**
    *   Convert categorical features (e.g., `gender`, `ethnicity`) into numerical format using one-hot encoding or similar methods.
3.  **Feature Scaling:**
    *   Standardize or normalize numerical features as required by the models.
4.  **Feature Transformation:**
    *   Apply transformations like log or Box-Cox for skewed distributions.

## Phase 3: Model Building

1.  **Data Splitting:** Split the data into training and testing sets, ensuring proper stratification.
2.  **Implement Baseline Models:**
    *   **Binary Classification:** Logistic Regression (Logit GLM).
    *   **Survival Analysis:** Cox Proportional Hazards (Cox PH) model with elastic-net regularization.
3.  **Implement Advanced Models:**
    *   **Binary Classification:** Gradient Boosted Decision Trees (e.g., XGBoost, LightGBM), BART.
    *   **Survival Analysis:** AFT models, DeepSurv, SurvFormer.
4.  **Energy-based MaxEnt Score:**
    *   Derive energy terms for the MaxEnt baseline model.

## Phase 4: Model Evaluation & Interpretation

1.  **Performance Metrics:**
    *   **Binary Models:** AUROC, Brier score, Precision-Recall AUC, Calibration slope.
    *   **Survival Models:** Concordance-index (C-index), time-dependent AUROC.
2.  **Model Calibration:**
    *   Plot calibration curves to check if predicted probabilities are well-calibrated.
3.  **Model Interpretation:**
    *   Use techniques like SHAP (SHapley Additive exPlanations) to explain model predictions.
    *   Analyze feature importance plots.
4.  **Assumption Checks:**
    *   For Cox models, test the proportional hazards assumption using Schoenfeld residuals.
    *   Check for outliers and high-leverage points.

## Phase 5: Reproducibility & Reporting

1.  **Experiment Logging:** Maintain a detailed log of all experiments in `SA_AKI_ML_Experiment_Log.md`.
2.  **Changelog:** Keep `Changelog.md` updated with all significant changes.
3.  **Fairness Audit:** Analyze model performance across different subgroups (e.g., gender, ethnicity).
4.  **Thesis Writing:**
    *   Generate plots, tables, and figures for the thesis.
    *   Write up the methodology, results, and discussion sections.
