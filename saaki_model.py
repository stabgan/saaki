"""SA-AKI mortality prediction pipeline.

Trains CatBoost and logistic-regression models on the MIMIC-IV SA-AKI cohort
and reports AUROC on a stratified 80/20 test split (CatBoost) and via
cross-validation (logistic regression).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Resolve data path relative to *this* script so the project works
# regardless of the caller's working directory.
_SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = _SCRIPT_DIR / "data" / "mimic_saaki_final.csv"

# ID columns that must be excluded to prevent data leakage
ID_COLS = ["stay_id", "subject_id", "hadm_id"]


def load_data(path: Path = DATA_PATH) -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Load the SA-AKI cohort CSV and return features, labels, and categorical column names.

    Steps:
        1. Drop target / time-to-event columns from features.
        2. Drop identifier columns to prevent data leakage.
        3. Drop columns with >99 % missing values.
        4. Fill NaN in categoricals with ``'NA'`` before casting to ``str``.

    Returns:
        ``(X, y, cat_cols)``
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}\n"
            "Place the MIMIC-IV SA-AKI cohort CSV in the data/ directory."
        )

    df = pd.read_csv(path)
    y = df["event_observed"].astype(int)
    X = df.drop(columns=["event_observed", "time_to_event_hrs"])

    # Drop identifier columns to prevent data leakage
    X = X.drop(columns=[c for c in ID_COLS if c in X.columns])

    # Drop columns missing >99 %
    missing = X.isnull().mean()
    X = X.drop(columns=missing[missing > 0.99].index)

    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    for c in cat_cols:
        # fillna first, then convert — avoids NaN becoming literal 'nan'
        X[c] = X[c].fillna("NA").astype(str)

    log.info(
        "Loaded %d rows, %d features (%d categorical).",
        len(X),
        X.shape[1],
        len(cat_cols),
    )
    return X, y, cat_cols


def train_test_auc() -> float:
    """Train a CatBoost classifier and return the test AUROC.

    Uses a stratified 80/20 split with ``random_state=42``.
    """
    X, y, cat_cols = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )

    train_pool = Pool(X_train, y_train, cat_features=cat_cols)
    test_pool = Pool(X_test, y_test, cat_features=cat_cols)

    model = CatBoostClassifier(
        iterations=1000,
        learning_rate=0.05,
        depth=6,
        l2_leaf_reg=3,
        loss_function="Logloss",
        eval_metric="AUC",
        verbose=False,
        random_seed=42,
    )
    model.fit(train_pool)

    pred = model.predict_proba(test_pool)[:, 1]
    auc = roc_auc_score(y_test, pred)
    log.info("CatBoost test AUROC: %.3f", auc)
    return auc


def logistic_cv_auc(cv: int = 3) -> float:
    """Run logistic regression with cross-validation and return mean AUROC."""
    X, y, cat_cols = load_data()
    num_cols = [c for c in X.columns if c not in cat_cols]

    preprocessor = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                num_cols,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                cat_cols,
            ),
        ]
    )

    clf = Pipeline(
        [
            ("preprocess", preprocessor),
            (
                "model",
                LogisticRegression(max_iter=1000, n_jobs=-1, solver="lbfgs"),
            ),
        ]
    )

    scores = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    mean_auc = float(scores.mean())
    log.info(
        "Logistic CV AUROC: %.3f ± %.3f",
        mean_auc,
        scores.std(),
    )
    return mean_auc


if __name__ == "__main__":
    logistic_cv_auc()
    train_test_auc()
