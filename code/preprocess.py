import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the original dataset
df = pd.read_csv('data/mimic_saaki_final.csv')

# --- Feature Selection: Drop high-missing columns ---
missing_values = df.isnull().mean() * 100
high_missing_cols = missing_values[missing_values > 95].index.tolist()
df_cleaned = df.drop(columns=high_missing_cols)
df_cleaned.to_csv('data/mimic_saaki_cleaned.csv', index=False)


# --- Preprocessing ---
# Separate features and target
X = df_cleaned.drop(columns=['event_observed', 'time_to_event_hrs'])
y = df_cleaned[['event_observed', 'time_to_event_hrs']]

# Identify numerical and categorical features
numerical_features = X.select_dtypes(include=['number']).columns.tolist()
categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

# Impute missing values
for col in numerical_features:
    median_val = X[col].median()
    X[col] = X[col].fillna(median_val)

for col in categorical_features:
    mode_val = X[col].mode()[0]
    X[col] = X[col].fillna(mode_val)

# One-hot encode categorical features
X = pd.get_dummies(X, columns=categorical_features, drop_first=True)

# Scale numerical features
scaler = StandardScaler()
# Get the list of numerical columns again after one-hot encoding
numerical_features_after_encoding = X.select_dtypes(include=['number']).columns.tolist()
# Ensure we only scale the original numerical features
original_numerical_to_scale = [f for f in numerical_features if f in numerical_features_after_encoding]

X[original_numerical_to_scale] = scaler.fit_transform(X[original_numerical_to_scale])

# Combine preprocessed features and target
preprocessed_df = pd.concat([X, y], axis=1)

# Save the preprocessed data
preprocessed_df.to_csv('data/mimic_saaki_preprocessed.csv', index=False)

print("Preprocessing complete. High-missing columns dropped and data preprocessed.")
print(f"Preprocessed data saved to data/mimic_saaki_preprocessed.csv")
