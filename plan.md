# Plan

- Explore dataset: evaluate missing values, feature distribution.
- Experiment with tree-based models (CatBoost, LightGBM) using categorical handling and missing value support.
- Use cross-validation to tune hyperparameters and attempt to push AUROC towards >0.90.
- Monitor for potential data leakage: only use features available within first 24h window.
- Future steps: feature engineering, missingness indicators, ensemble methods, and fairness audits as per README guidance.

- Attempted CatBoost, LightGBM, and XGBoost models with increased iterations and cross-validation. Best AUROC ~0.80.
- Need feature engineering (e.g., missingness indicators, interaction terms) to potentially reach ≥0.85.
- Added logistic regression baseline using a column transformer and cross-validation to benchmark linear model performance.
