import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# Store model performance
results = []

def evaluate_model(model_name, y_true, y_pred):
    """
    Evaluate a machine learning model and store its performance.
    """

    report = classification_report(
        y_true,
        y_pred,
        output_dict=True
    )

    accuracy = accuracy_score(y_true, y_pred)

    print("\nAccuracy:", round(accuracy, 4))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))

    results.append({
        "Model": model_name,
        "Accuracy": round(accuracy, 4),
        "Precision": round(report["1"]["precision"], 4),
        "Recall": round(report["1"]["recall"], 4),
        "F1 Score": round(report["1"]["f1-score"], 4)
    })



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

evaluate_model(
    "Logistic Regression",
    y_test,
    y_pred
)

# ======================================================
# Decision Tree Classifier
# ======================================================

print("\n" + "=" * 50)
print("Training Decision Tree Classifier")
print("=" * 50)

# Create Decision Tree model
decision_tree = DecisionTreeClassifier(
    random_state=42
)

# Train model
decision_tree.fit(X_train_scaled, y_train)

# Make predictions
dt_predictions = decision_tree.predict(X_test_scaled)
# ======================================================
# Calculate accuracy
#======================================================
evaluate_model(
    "Decision Tree",
    y_test,
    dt_predictions
)


# ======================================================
# Random Forest Classifier
# ======================================================

print("\n" + "=" * 50)
print("Training Random Forest Classifier")
print("=" * 50)

# Create Random Forest model
random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
random_forest.fit(X_train_scaled, y_train)

# Make predictions
rf_predictions = random_forest.predict(X_test_scaled)

# =====================================================
# Calculate accuracy
# ====================================================
evaluate_model(
    "Random Forest",
    y_test,
    rf_predictions
)


# ======================================================
# K-Nearest Neighbors (KNN)
# ======================================================

print("\n" + "=" * 50)
print("Training K-Nearest Neighbors (KNN)")
print("=" * 50)

# Create KNN model
knn_model = KNeighborsClassifier(n_neighbors=5)

# Train model
knn_model.fit(X_train_scaled, y_train)

# Make predictions
knn_predictions = knn_model.predict(X_test_scaled)

# =====================================================
# Calculate accuracy
# ===================================================
evaluate_model(
    "K-Nearest Neighbors",
    y_test,
    knn_predictions
)


# ======================================================
# Support Vector Machine (SVM)
# ======================================================

print("\n" + "=" * 50)
print("Training Support Vector Machine (SVM)")
print("=" * 50)

# Create SVM model
svm_model = SVC(
    kernel="rbf",
    random_state=42
)

# Train model
svm_model.fit(X_train_scaled, y_train)

# Make predictions
svm_predictions = svm_model.predict(X_test_scaled)

# =====================================================
# Calculate accuracy
# ====================================================
evaluate_model(
    "Support Vector Machine",
    y_test,
    svm_predictions
)




# ======================================================
# Model Comparison
# ======================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Accuracy",
    ascending=False
)

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(results_df)

print("=" * 60)




# ======================================================
# Save Best Model
# ======================================================

joblib.dump(random_forest, "models/random_forest_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("\n" + "=" * 50)
print("Best model and scaler saved successfully!")
print("=" * 50)