import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import OneHotEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import StackingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

# load data
DATA_PATH = 'data/mimic_saaki_final.csv'

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    y = df['event_observed'].astype(int)
    X = df.drop(columns=['event_observed', 'time_to_event_hrs'])
    # drop columns missing >99%
    missing = X.isnull().mean()
    X = X.drop(columns=missing[missing > 0.99].index)
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    num_cols = X.columns.difference(cat_cols).tolist()
    for c in cat_cols:
        X[c] = X[c].astype(str).fillna('NA')
    return X, y, num_cols, cat_cols

def baseline_catboost_auc():
    """Return AUROC using plain CatBoost (baseline)."""
    X, y, _, cat_cols = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
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
    model.fit(X_train, y_train, cat_features=cat_cols)
    pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, pred)
    print(f'Baseline CatBoost AUROC: {auc:.3f}')

def stacking_auc():
    """Train stacking ensemble with log-normalisation."""
    X, y, num_cols, cat_cols = load_data()

    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('power', PowerTransformer(method='yeo-johnson')),
    ])
    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])
    preprocessor = ColumnTransformer([
        ('num', numeric_pipeline, num_cols),
        ('cat', categorical_pipeline, cat_cols),
    ])

    estimators = [
        ('xgb', XGBClassifier(eval_metric='auc', use_label_encoder=False, n_estimators=300, learning_rate=0.05, max_depth=6)),
        ('lgbm', LGBMClassifier(objective='binary', n_estimators=300, learning_rate=0.05)),
    ]
    clf = StackingClassifier(
        estimators=estimators,
        final_estimator=LGBMClassifier(objective='binary', n_estimators=200),
        passthrough=False,
    )
    model = Pipeline([
        ('prep', preprocessor),
        ('clf', clf),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, pred)
    print(f'Stacking Ensemble AUROC: {auc:.3f}')

if __name__ == '__main__':
    stacking_auc()
