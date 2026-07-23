import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Load the dataset
df = pd.read_csv("data/diabetes.csv")

# Display basic information
print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)

# Display the first 5 rows
print(df.head())

# ======================================================
# Data Cleaning and Preprocessing
# ======================================================


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


# Separate features and target variable
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)


# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Features Shape:", X_train.shape)
print("Testing Features Shape:", X_test.shape)
print("Training Labels Shape:", y_train.shape)
print("Testing Labels Shape:", y_test.shape)

# ======================================================
# Feature Scaling
# ======================================================

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform it
X_train_scaled = scaler.fit_transform(X_train)

# Transform the test data using the same scaler
X_test_scaled = scaler.transform(X_test)

# Verify the scaled data shapes
print("\nScaled Training Shape:", X_train_scaled.shape)
print("Scaled Testing Shape:", X_test_scaled.shape)

# Verify scaling statistics
print("\nMean of Scaled Training Data:")
print(X_train_scaled.mean(axis=0))

print("\nStandard Deviation of Scaled Training Data:")
print(X_train_scaled.std(axis=0))

# ======================================================
# Model Training and Evaluation
# ======================================================

# ======================================================
# Logistic Regression Model
# ======================================================

print("\n" + "=" * 50)
print("Training Logistic Regression Model")
print("=" * 50)

# Create model
logistic_model = LogisticRegression(random_state=42)

# Train model
logistic_model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = logistic_model.predict(X_test_scaled)

# ======================================================
# Model Evaluation
# ======================================================

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

