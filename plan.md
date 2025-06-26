# Plan

- Explore dataset: evaluate missing values, feature distribution.
- Experiment with tree-based models (CatBoost, LightGBM) using categorical handling and missing value support.
- Use cross-validation to tune hyperparameters and attempt to push AUROC towards >0.90.
- Monitor for potential data leakage: only use features available within first 24h window.
- Future steps: feature engineering, missingness indicators, ensemble methods, and fairness audits as per README guidance.

- Attempted CatBoost, LightGBM, and XGBoost models with increased iterations and cross-validation. Best AUROC ~0.80.
- Need feature engineering (e.g., missingness indicators, interaction terms) to potentially reach ≥0.85.

- New step: add numeric power transformations (Yeo-Johnson) to normalise skewed
  distributions and one-hot encode categorical fields.
- Build a stacking ensemble combining XGBoost and LightGBM with an LGBM
  meta-classifier. Evaluate on holdout AUROC aiming for improvement beyond 0.80.
