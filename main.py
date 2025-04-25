import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, f_oneway
from scipy import stats

def detect_outliers(df, column):
    # Calculate the IQR for the given column
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    # Define outlier condition: values outside 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Identify outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return len(outliers), len(df)

def missing_value_percentage(df):
    # Calculate the percentage of missing values for each column
    missing_values = df.isnull().sum() / len(df) * 100
    return missing_values

def clean_and_analyze_data(bmi_file, info_file):
    # 1. Load the CSV files
    df_bmi = pd.read_csv(bmi_file, sep=";", on_bad_lines="skip")
    df_info = pd.read_csv(info_file, sep=";", on_bad_lines="skip")

    # 2. Clean df_bmi: Rename columns and handle missing values
    df_bmi_clean = df_bmi[['ad-soyad', 'ameliyat tipi', '0', '1', '2']].copy()
    df_bmi_clean.columns = ['ad_soyad', 'surgery_type', 'BMI_0', 'BMI_1', 'BMI_2']
    df_bmi_clean['BMI_0'] = pd.to_numeric(df_bmi_clean['BMI_0'].str.replace(',', '.'), errors='coerce')
    df_bmi_clean['BMI_1'] = pd.to_numeric(df_bmi_clean['BMI_1'].str.replace(',', '.'), errors='coerce')
    df_bmi_clean['BMI_2'] = pd.to_numeric(df_bmi_clean['BMI_2'].str.replace(',', '.'), errors='coerce')
    df_bmi_clean.dropna(subset=['BMI_0', 'BMI_1', 'BMI_2'], inplace=True)

    # Calculate BMI difference and monthly loss
    df_bmi_clean['BMI_diff'] = df_bmi_clean['BMI_0'] - df_bmi_clean['BMI_2']
    df_bmi_clean['monthly_BMI_loss'] = df_bmi_clean['BMI_diff'] / 3

    # 3. Clean df_info: Ensure 'age' column is numeric
    df_info_clean = df_info[['yaş', 'ameliyat tipi', 'hba1c', 'insülin', 'c-peptit']].iloc[:len(df_bmi_clean)].reset_index(drop=True)
    df_info_clean['yaş'] = pd.to_numeric(df_info_clean['yaş'].str.replace(',', '.'), errors='coerce')

    # 4. Merge the two dataframes
    df_merged = pd.concat([df_bmi_clean.reset_index(drop=True), df_info_clean], axis=1)
    df_merged.dropna(subset=['yaş', 'monthly_BMI_loss'], inplace=True)

    # 5. Boxplot: BMI loss by surgery type
    df_merged['surgery_type'] = df_merged['surgery_type'].astype(str)
    plot_data = df_merged.dropna(subset=['surgery_type', 'monthly_BMI_loss'])

    if not plot_data.empty:
        sns.boxplot(data=plot_data, x='surgery_type', y='monthly_BMI_loss')
        plt.title("Monthly BMI Loss by Surgery Type")
        plt.xlabel("Surgery Type")
        plt.ylabel("Monthly BMI Loss")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("⚠️ Warning: Not enough data to create boxplot.")

    # 6. Boxplots for Clinical Variables
    for var in ['hba1c', 'insülin', 'c-peptit']:
        df_merged[var] = pd.to_numeric(df_merged[var], errors='coerce')
        temp = df_merged.dropna(subset=[var])
        if len(temp) > 2:
            sns.boxplot(data=temp, x='surgery_type', y=var)
            plt.title(f"Monthly {var.upper()} by Surgery Type")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    # 7. Scatter: Age vs BMI loss
    sns.regplot(data=df_merged, x='yaş', y='monthly_BMI_loss')
    plt.title("Age vs Monthly BMI Loss")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 8. Pearson Correlation with Hypothesis Testing
    df_merged['yaş'] = pd.to_numeric(df_merged['yaş'], errors='coerce')
    df_merged.dropna(subset=['yaş', 'monthly_BMI_loss'], inplace=True)

    corr_matrix = df_merged[['yaş', 'monthly_BMI_loss']].corr()
    corr, p_val = pearsonr(df_merged['yaş'], df_merged['monthly_BMI_loss'])

    # Hypothesis testing for Surgery type and Age effects
    # Null Hypothesis: Surgery type and age have no effect on monthly BMI loss
    # Alternative Hypothesis: Surgery type and age have a significant effect on monthly BMI loss
    surgery_type_data = df_merged['surgery_type'].unique()
    groups = [df_merged[df_merged['surgery_type'] == surgery]['monthly_BMI_loss'] for surgery in surgery_type_data]
    f_stat, p_value_anova = f_oneway(*groups)

    hypothesis_result_anova = "Reject the null hypothesis: Surgery type and/or age significantly affect monthly BMI loss." if p_value_anova < 0.05 else "Fail to reject the null hypothesis: No significant effect of surgery type and/or age on monthly BMI loss."

    # Outlier detection
    outlier_bmi_0, total_bmi_0 = detect_outliers(df_merged, 'BMI_0')
    outlier_bmi_1, total_bmi_1 = detect_outliers(df_merged, 'BMI_1')
    outlier_bmi_2, total_bmi_2 = detect_outliers(df_merged, 'BMI_2')
    outlier_bmi_loss, total_bmi_loss = detect_outliers(df_merged, 'monthly_BMI_loss')

    # Missing value percentage
    missing_values = missing_value_percentage(df_merged)

    # Create a table for results
    correlation_table = pd.DataFrame({
        'Correlation Coefficient (r)': [corr],
        'p-value (Pearson)': [p_val],
        'Hypothesis Test Result (Pearson)': ["Reject" if p_val < 0.05 else "Fail to reject"],
        'ANOVA p-value (Surgery Type and Age)': [p_value_anova],
        'Hypothesis Test Result (ANOVA)': [hypothesis_result_anova],
        'Missing Value (%) - BMI_0': [missing_values['BMI_0']],
        'Missing Value (%) - BMI_1': [missing_values['BMI_1']],
        'Missing Value (%) - BMI_2': [missing_values['BMI_2']],
        'Missing Value (%) - Monthly BMI Loss': [missing_values['monthly_BMI_loss']],
        'Outliers - BMI_0': [outlier_bmi_0 / total_bmi_0 * 100],
        'Outliers - BMI_1': [outlier_bmi_1 / total_bmi_1 * 100],
        'Outliers - BMI_2': [outlier_bmi_2 / total_bmi_2 * 100],
        'Outliers - Monthly BMI Loss': [outlier_bmi_loss / total_bmi_loss * 100]
    })

    # Display correlation matrix and results table
    if len(df_merged[['yaş', 'monthly_BMI_loss']].dropna()) >= 2:
        # Correlation Matrix
        plt.figure(figsize=(5, 4))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Matrix")
        plt.tight_layout()
        plt.show()

        print("Correlation Matrix:\n", corr_matrix)
        print(f"Pearson r: {corr:.3f}, p-value: {p_val:.3f}")
        print("Hypothesis Testing Result (Pearson):", "Reject" if p_val < 0.05 else "Fail to reject")
        print("\nANOVA Test Result (Surgery Type and Age):", hypothesis_result_anova)
        print("\nCorrelation, Missing Values, and Outlier Table:\n", correlation_table)
    else:
        print("⚠️ Warning: Not enough data for Pearson correlation.")

# Example of usage:
bmi_file = '/content/ayaybmi.csv'  # Replace with your file path
info_file = '/content/TAKİP 22.01.2025 SPSSE HAZIRLIK (1).csv'  # Replace with your file path

clean_and_analyze_data(bmi_file, info_file)
