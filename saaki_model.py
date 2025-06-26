import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# load data
DATA_PATH = 'data/mimic_saaki_final.csv'

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    y = df['event_observed'].astype(int)
    X = df.drop(columns=['event_observed'])
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

if __name__ == '__main__':
    train_test_auc()
