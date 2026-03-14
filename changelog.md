# v1.3.0
- Modernized `saaki_model.py`:
  - Resolved data path relative to script location (`pathlib.Path`) so the project works regardless of working directory
  - Added `FileNotFoundError` with helpful message when data file is missing
  - Added structured logging (`logging` module) replacing bare `print()` calls
  - Added module docstring, function docstrings, and type hints
  - Functions now return AUROC values for programmatic use
  - Reordered imports per PEP 8 (stdlib → third-party → local)
- Expanded `.gitignore` to cover `__pycache__/`, `catboost_info/`, IDE files, OS files
- Verified all sklearn / CatBoost / pandas APIs against latest docs via Context7 — no deprecated calls found

# v1.2.0
- Fixed ID column leakage: `stay_id`, `subject_id`, `hadm_id` now explicitly dropped before training
- Fixed NaN handling in categoricals: `.fillna('NA').astype(str)` instead of `.astype(str).fillna('NA')` which silently converted NaN to literal string 'nan'
- Cleaned `requirements.txt`: removed deprecated `pickle5`, `pandas-profiling` (→ `ydata-profiling`), `pysurvival`, and unused heavy dependencies (TensorFlow, PyTorch, etc.)
- Rewrote README.md with modern formatting, tech stack, known issues, and clear methodology section

# v1.0.0
- added plan.md and saaki_model.py for CatBoost-based binary classification.
- Achieved Test AUROC: 0.794 on catboost

# v1.0.1
- Tested multiple models (CatBoost, LightGBM, XGBoost) with hyperparameter tuning and cross-validation.
- Best AUROC remained around 0.80; unable to reach target 0.85 yet.

# v1.1.0
- Added logistic regression baseline with column transformer pipeline and 3-fold cross-validation.
- Logistic CV AUROC ~0.75; CatBoost test AUROC unchanged at ~0.79.
