# dsaproposal
DSA210 project proposal

Motivation: Why are you working on this project?

  I think that medical technology is a work space that we should develop as a country. Right now I am trying to code an AI Agent that analyzes this data and give doctors some hypothesis     with causation and correlation using SPSS methods, so finishing this project is a motivation for me as well.
  
Data Source: Where did you get this data? How did you collect it?

  I have found a dataset that consists of 2532 obese people who got into bariatric surgery. This dataset consists of their age, gender, operation type, whether there are extra operations    or not, and their values of insulin and pepdide. The dataset also keeps track of their height § weight after the operation in a time frame. This data was collected by my father who is     a surgeon.
  
Data Analysis: Techniques used, different stages of analysis

  I use ML & SPSS methods. Firstly I use destrciptive analysis -for extraction and summary of the dataset- then I use correlation analysis (Pearson, chi-square, etc.) -to decide to which    hypothesis to write on / whether there is correlation or not- then data visualization which is a form of ML and lastly I use SPSS to identify the dataset and prove mty hypothesis to be    true or false.
  
Findings: What are the interesting findings that you found in this project?

  Looking other people's lives as number is a thing that I find interesting in the first place - however, it is too general - if you want me to be spesific through this project some         people's before and after was quite interesting, like how could an enormous change like that could happen in just 3-4 months.
  
Limitations and Future Work: What could be done better? Do you have any future plans on your project?

  As I said I want to continue to this project as making it an AI Agent and working on how to sell that. However, I want to achieve that with the informations I've learned thorough this     lesson. I think that if I've added some diet plans and image estimators (ex. you will look like this in 3 months (with ML) ), and make it publicly available I could've made a system for   the good of both patients and doctors.

Monthly BMI Loss Analysis and Hypothesis Testing
This repository contains an analysis of the relationship between age and monthly BMI loss across different surgery types. The analysis includes the following steps:

Data Preparation:

The dataset contains information about patients who underwent various weight loss surgeries, including their BMI at different stages and clinical variables such as age, hba1c, insulin, and c-peptit.

The dataset was cleaned to remove missing values, and BMI changes were calculated between initial and final measurements.

Hypothesis Testing:

Null Hypothesis (H₀): Surgery type and age have no effect on the monthly BMI change.

Alternative Hypothesis (H₁): Surgery type and age have a significant effect on the monthly BMI change.

Two tests were performed:

Pearson Correlation Test: To check the relationship between age and monthly BMI loss.

ANOVA Test: To test whether surgery type and/or age significantly affect the monthly BMI loss.

Outlier Detection and Missing Values:

Outliers were detected using the Interquartile Range (IQR) method, and their percentage was calculated for each relevant variable.

Missing value percentages were also calculated for each variable to assess data quality.

Results
Pearson Correlation:
The Pearson correlation coefficient between age and monthly BMI loss is -0.129, with a p-value of 0.255, indicating no significant relationship between these two variables.

ANOVA Test (Surgery Type and Age):
The p-value for the ANOVA test is 0.9168, which is greater than 0.05, indicating that surgery type and age do not significantly affect monthly BMI loss.

Missing Values:
No missing values were found in the relevant columns (BMI_0, BMI_1, BMI_2, monthly_BMI_loss).

Outliers:
Outliers were found in the BMI variables, with the highest percentage of outliers in BMI_2 (8.75%) and monthly BMI loss (8.75%).

Plots
1. Correlation Matrix:
The correlation matrix shows a very weak negative correlation between age and monthly BMI loss.

Ekran Resmi 2025-04-25 21.15.06.png

2. Scatter Plot: Age vs Monthly BMI Loss
This plot visualizes the relationship between age and monthly BMI loss. The regression line shows a slight downward trend, indicating a weak negative correlation.



3. Boxplot: Monthly BMI Loss by Surgery Type
This boxplot shows the distribution of monthly BMI loss for different surgery types. The data reveals some variations across surgeries, with outliers present in certain types.



Files in the Repository

main.py: The Python script that contains the full analysis, including data cleaning, hypothesis testing, and visualization.

data.csv: The raw dataset containing patient information and BMI values.

README.md: This file, containing an overview of the analysis and results.

  
  
