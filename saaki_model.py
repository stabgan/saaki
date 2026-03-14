import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer

# load data
DATA_PATH = 'data/mimic_saaki_final.csv'

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    y = df['event_observed'].astype(int)
    X = df.drop(columns=['event_observed','time_to_event_hrs'])
    # drop columns missing >99%
    missing = X.isnull().mean()
    X = X.drop(columns=missing[missing > 0.99].index)
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    for c in cat_cols:
        X[c] = X[c].astype(str).fillna('NA')
    return X, y, cat_cols

def train_test_auc():
    X, y, cat_cols = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    train_pool = Pool(X_train, y_train, cat_features=cat_cols)
    test_pool = Pool(X_test, y_test, cat_features=cat_cols)
    model = CatBoostClassifier(
        iterations=1000,
        learning_rate=0.05,
        depth=6,
        l2_leaf_reg=3,
        loss_function='Logloss',
        eval_metric='AUC',
        verbose=False,
        random_seed=42,
    )
    model.fit(train_pool)
    pred = model.predict_proba(test_pool)[:, 1]
    auc = roc_auc_score(y_test, pred)
    print(f'Test AUROC: {auc:.3f}')

def logistic_cv_auc(cv: int = 3):
    """Run logistic regression with cross-validation and report AUROC."""
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
                        (
                            "onehot",
                            OneHotEncoder(handle_unknown="ignore"),
                        ),
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
    print(
        f"Logistic CV AUROC: {scores.mean():.3f} \u00b1 {scores.std():.3f}"
    )

if __name__ == '__main__':
    logistic_cv_auc()
    train_test_auc()
