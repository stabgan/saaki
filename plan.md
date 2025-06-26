# Plan

- Explore dataset: evaluate missing values, feature distribution.
- Experiment with tree-based models (CatBoost, LightGBM) using categorical handling and missing value support.
- Use cross-validation to tune hyperparameters and attempt to push AUROC towards >0.90.
- Monitor for potential data leakage: only use features available within first 24h window.
- Future steps: feature engineering, missingness indicators, ensemble methods, and fairness audits as per README guidance.
