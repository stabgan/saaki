import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
import xgboost as xgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

df = pd.read_csv('data/mimic_saaki_preprocessed.csv')

# --- Data Preparation ---
X = df.drop(columns=['event_observed', 'time_to_event_hrs'])
y = df['event_observed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- XGBoost Hyperparameter Tuning with Bayesian Optimization ---

# Define the search space for hyperparameters
space = {
    'n_estimators': hp.quniform('n_estimators', 100, 1000, 50),
    'max_depth': hp.quniform('max_depth', 3, 10, 1),
    'learning_rate': hp.uniform('learning_rate', 0.01, 0.2),
    'subsample': hp.uniform('subsample', 0.7, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.7, 1.0),
    'gamma': hp.uniform('gamma', 0, 0.5),
    'scale_pos_weight': (y_train == 0).sum() / (y_train == 1).sum()
}

# Define the objective function to minimize
def objective(params):
    params['n_estimators'] = int(params['n_estimators'])
    params['max_depth'] = int(params['max_depth'])
    
    clf = xgb.XGBClassifier(
        **params,
        tree_method='gpu_hist',  # Use GPU acceleration
        objective='binary:logistic',
        eval_metric='auc',
        use_label_encoder=False,
        random_state=42
    )
    
    # Use 5-fold cross-validation
    score = cross_val_score(clf, X_train, y_train, cv=5, scoring='roc_auc', n_jobs=-1).mean()
    
    # We want to maximize ROC AUC, so we return -score
    return {'loss': -score, 'status': STATUS_OK}

# Run the Bayesian optimization
trials = Trials()
best = fmin(
    fn=objective,
    space=space,
    algo=tpe.suggest,
    max_evals=100, # Number of iterations
    trials=trials
)

print("\n--- Best Hyperparameters Found ---")
print(best)

# --- Train Final XGBoost Model with Best Hyperparameters ---

# Convert float hyperparameters to int where necessary
best['n_estimators'] = int(best['n_estimators'])
best['max_depth'] = int(best['max_depth'])

final_xgb = xgb.XGBClassifier(
    **best,
    tree_method='gpu_hist',  # Use GPU acceleration
    objective='binary:logistic',
    eval_metric='auc',
    use_label_encoder=False,
    scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),
    random_state=42
)

final_xgb.fit(X_train, y_train)

# Make predictions
y_pred_proba_final = final_xgb.predict_proba(X_test)[:, 1]

# Evaluate the final model
roc_auc_final = roc_auc_score(y_test, y_pred_proba_final)
brier_score_final = brier_score_loss(y_test, y_pred_proba_final)

print("\n--- XGBoost Results (After Tuning) ---")
print(f"AUROC: {roc_auc_final:.4f}")
print(f"Brier Score: {brier_score_final:.4f}")
