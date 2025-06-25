import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('data/mimic_saaki_cleaned.csv')

# --- Descriptive Statistics ---
with open('doc/descriptive_stats.txt', 'w') as f:
    f.write(df.describe(include='all').to_string())

# --- Missing Value Analysis ---
missing_values = df.isnull().mean() * 100
with open('doc/missing_values.txt', 'w') as f:
    f.write(missing_values.to_string())

# --- Plotting ---
# Identify numerical and categorical features
numerical_features = df.select_dtypes(include=['number']).columns.tolist()
categorical_features = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Histograms
for feature in numerical_features:
    plt.figure(figsize=(10, 6))
    df[feature].hist(bins=50)
    plt.title(f'Histogram of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
    plt.savefig(f'plots/histograms/{feature}_hist.png')
    plt.close()

# Bar plots
for feature in categorical_features:
    plt.figure(figsize=(10, 6))
    df[feature].value_counts().plot(kind='bar')
    plt.title(f'Bar Plot of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'plots/bar_plots/{feature}_bar.png')
    plt.close()

# Violin plots
for feature in numerical_features:
    plt.figure(figsize=(12, 7))
    sns.violinplot(x='event_observed', y=feature, data=df, inner='quartile', split=True)
    plt.title(f'Violin Plot of {feature} by Outcome')
    plt.xlabel('Event Observed (0 = Survival, 1 = Death)')
    plt.ylabel(feature)
    plt.savefig(f'plots/violin_plots/{feature}_violin.png')
    plt.close()

# --- Correlation Analysis ---
numerical_df = df.select_dtypes(include=['number'])
correlation_matrix = numerical_df.corr()
correlation_matrix.to_csv('doc/correlation_matrix.csv')

plt.figure(figsize=(20, 15))
sns.heatmap(correlation_matrix, cmap='coolwarm')
plt.title('Correlation Matrix of Numerical Features')
plt.tight_layout()
plt.savefig('plots/correlation_heatmap.png')
plt.close()

print("EDA re-run on cleaned data is complete.")
