import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("data/diabetes.csv")

# Display basic information
print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)

# Display the first 5 rows
print(df.head())

#Identify Invalid Zero Values
# Columns that should not contain zero values
zero_columns = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]

print("\nInvalid Zero Values:")

for col in zero_columns:
    zero_count = (df[col] == 0).sum()
    print(f"{col}: {zero_count}")

# Replace invalid zero values with NaN
df[zero_columns] = df[zero_columns].replace(0, np.nan)
print("\nMissing Values After Replacing Invalid Zeros:")

print(df.isnull().sum())


# Fill missing values using the median
for col in zero_columns:
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)

print("\nMissing Values After Median Imputation:")
print(df.isnull().sum())


# Check for duplicate rows
duplicate_count = df.duplicated().sum()

print("\nDuplicate Records:", duplicate_count)