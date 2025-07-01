# v1.0.0
- added plan.md and saaki_model.py for CatBoost-based binary classification.
- Achieved Test AUROC: 0.794 on catboost

# v1.0.1
- Tested multiple models (CatBoost, LightGBM, XGBoost) with hyperparameter tuning and cross-validation.
- Best AUROC remained around 0.80; unable to reach target 0.85 yet.

# v1.1.0
- Added logistic regression baseline with column transformer pipeline and 3-fold cross-validation.
- Logistic CV AUROC ~0.75; CatBoost test AUROC unchanged at ~0.79.
