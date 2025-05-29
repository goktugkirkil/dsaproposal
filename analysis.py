## this code block is used for all the graphs and drawings in Final_Report.md file.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
from scipy.stats import f_oneway, ttest_ind

# Read CSV files containing BMI and clinical data
df_bmi = pd.read_csv("ayaybmi.csv", sep=";", on_bad_lines="skip")
df_info = pd.read_csv("TAKI\u0307P 22.01.2025 SPSSE HAZIRLIK (1).csv", sep=";", on_bad_lines="skip")

# Select and clean relevant BMI columns
df_bmi_clean = df_bmi[['ad-soyad', 'ameliyat tipi', '0', '1', '2']].copy()
df_bmi_clean.columns = ['ad_soyad', 'surgery_type', 'BMI_0', 'BMI_1', 'BMI_2']

# Convert BMI values to numeric format
for col in ['BMI_0', 'BMI_1', 'BMI_2']:
    df_bmi_clean[col] = pd.to_numeric(df_bmi_clean[col].str.replace(',', '.'), errors='coerce')

# Calculate total and monthly BMI loss
df_bmi_clean['BMI_diff'] = df_bmi_clean['BMI_0'] - df_bmi_clean['BMI_2']
df_bmi_clean['monthly_BMI_loss'] = df_bmi_clean['BMI_diff'] / 3

# Fill missing values with column mean
for col in ['BMI_0', 'BMI_1', 'BMI_2', 'monthly_BMI_loss']:
    df_bmi_clean[col].fillna(df_bmi_clean[col].mean(), inplace=True)

# Clean clinical information columns
df_info_clean = df_info[['ya\u015f', 'ameliyat tipi', 'hba1c', 'ins\u00fclin', 'c-peptit']].iloc[:len(df_bmi_clean)].reset_index(drop=True)
df_info_clean['ya\u015f'] = pd.to_numeric(df_info_clean['ya\u015f'].str.replace(',', '.'), errors='coerce')
df_info_clean['ya\u015f'].fillna(df_info_clean['ya\u015f'].mean(), inplace=True)

# Convert clinical variables to numeric and fill missing values
for col in ['hba1c', 'ins\u00fclin', 'c-peptit']:
    df_info_clean[col] = pd.to_numeric(df_info_clean[col].astype(str).str.replace(',', '.'), errors='coerce')
    df_info_clean[col].fillna(df_info_clean[col].mean(), inplace=True)

# Merge BMI and clinical datasets
df_merged = pd.concat([df_bmi_clean.reset_index(drop=True), df_info_clean], axis=1)

# Use only 'age' and 'monthly_BMI_loss' for modeling
X = df_merged[['ya\u015f']]
y = df_merged['monthly_BMI_loss']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define three regression models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

results = {}

# Train each model and evaluate performance
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    results[name] = {"MAE": mae, "RMSE": rmse, "R\u00b2": r2}

# Display model performance results
results_df = pd.DataFrame(results).T
print("Model Performance:")
print(results_df)

# Plot actual vs predicted values for each model
for name, model in models.items():
    y_pred_all = model.predict(X)
    plt.figure()
    sns.scatterplot(x=y, y=y_pred_all, alpha=0.6)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.xlabel("Actual Monthly BMI Loss")
    plt.ylabel("Predicted")
    plt.title(f"{name} \u2013 Predicted vs Actual")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Define numeric columns
numerical_cols = ['BMI_0', 'BMI_1', 'BMI_2', 'monthly_BMI_loss', 'ya\u015f', 'hba1c', 'ins\u00fclin', 'c-peptit']

# Plot distributions for each numerical variable
plt.figure(figsize=(15, 12))
for i, col in enumerate(numerical_cols):
    plt.subplot(3, 3, i + 1)
    sns.histplot(df_merged[col], kde=True)
    plt.title(f"Distribution of {col}")
plt.tight_layout()
plt.savefig("univariate_analysis.png")

# Scatter plot of age vs BMI loss by surgery type
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_merged, x='ya\u015f', y='monthly_BMI_loss', hue='surgery_type', alpha=0.6)
plt.title("Age vs Monthly BMI Loss (by Surgery Type)")
plt.grid(True)
plt.tight_layout()
plt.savefig("bivariate_analysis.png")

# Correlation heatmap for numeric variables
plt.figure(figsize=(10, 8))
corr_matrix = df_merged[numerical_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Numerical Variables")
plt.tight_layout()
plt.savefig("multivariate_analysis.png")

# Group age into categories for statistical tests
df_merged["age_group"] = pd.cut(df_merged["ya\u015f"], bins=[0, 40, 60, 100], labels=["Young", "Middle-aged", "Older"])

# Get monthly BMI loss for each age group
grouped_age = df_merged.groupby("age_group")["monthly_BMI_loss"]
age_groups = df_merged["age_group"].unique()

print("\n--- Statistical Test Based on Age Groups ---")

# Apply ANOVA if there are 3 age groups
if len(age_groups) >= 3:
    anova_age = f_oneway(*[group for name, group in grouped_age])
    print("ANOVA Test (Age Groups)")
    print("F-statistic:", anova_age.statistic)
    print("p-value:", anova_age.pvalue)

    if anova_age.pvalue < 0.05:
        print("Monthly BMI loss significantly differs between age groups (p < 0.05)")
    else:
        print("No significant difference between age groups (p \u2265 0.05)")

# Apply t-test if only 2 age groups exist
elif len(age_groups) == 2:
    g1 = df_merged[df_merged["age_group"] == age_groups[0]]["monthly_BMI_loss"]
    g2 = df_merged[df_merged["age_group"] == age_groups[1]]["monthly_BMI_loss"]
    t_stat, p_val = ttest_ind(g1, g2)
    print("T-test (Two Age Groups)")
    print(f"Groups: {age_groups[0]} vs {age_groups[1]}")
    print("T-statistic:", t_stat)
    print("p-value:", p_val)

    if p_val < 0.05:
        print("Significant difference found (p < 0.05)")
    else:
        print("No significant difference found (p \u2265 0.05)")
