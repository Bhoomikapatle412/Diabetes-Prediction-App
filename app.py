import streamlit as st
import pandas as pd
import joblib

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide"
)

# ======================================================
# Load Model and Scaler
# ======================================================

model = joblib.load("models/random_forest_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# ======================================================
# Sidebar
# ======================================================

st.sidebar.title("🩺 About")

st.sidebar.info("""
**Diabetes Prediction App**

This application predicts the likelihood of diabetes using a
Machine Learning model trained on the Pima Indians Diabetes Dataset.
""")

st.sidebar.markdown("---")

st.sidebar.subheader("Model Information")

st.sidebar.write("**Algorithm:** Random Forest")
st.sidebar.write("**Accuracy:** 77.92%")
st.sidebar.write("**Dataset:** Pima Indians Diabetes Dataset")

# ======================================================
# Main Page
# ======================================================

st.title("🩺 Diabetes Prediction App")

st.markdown("""
Welcome to the **Diabetes Prediction App**.

This application uses a **Machine Learning Random Forest model**
to predict whether a patient is likely to have diabetes based on
their health information.

Fill in the required details and click **Predict Diabetes**.
""")

st.divider()

st.subheader("📋 Enter Patient Information")

# ======================================================
# Input Fields
# ======================================================

col1, col2 = st.columns(2)

with col1:

    pregnancies = st.number_input(
        "Pregnancies",
        min_value=0,
        max_value=20,
        value=1
    )

    glucose = st.number_input(
        "Glucose",
        min_value=0,
        max_value=300,
        value=120
    )

    blood_pressure = st.number_input(
        "Blood Pressure",
        min_value=0,
        max_value=200,
        value=70
    )

    skin_thickness = st.number_input(
        "Skin Thickness",
        min_value=0,
        max_value=100,
        value=20
    )

with col2:

    insulin = st.number_input(
        "Insulin",
        min_value=0,
        max_value=900,
        value=80
    )

    bmi = st.number_input(
        "BMI",
        min_value=0.0,
        max_value=70.0,
        value=25.0
    )

    diabetes_pedigree = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.0,
        max_value=3.0,
        value=0.500,
        format="%.3f"
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=30
    )

st.divider()

# ======================================================
# Prediction Button
# ======================================================

if st.button("🔍 Predict Diabetes", use_container_width=True):

    # Create DataFrame
    input_data = pd.DataFrame({
        "Pregnancies": [pregnancies],
        "Glucose": [glucose],
        "BloodPressure": [blood_pressure],
        "SkinThickness": [skin_thickness],
        "Insulin": [insulin],
        "BMI": [bmi],
        "DiabetesPedigreeFunction": [diabetes_pedigree],
        "Age": [age]
    })

    # Scale Input
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    # Probability
    probability = model.predict_proba(input_scaled)[0][1]

    # ==================================================
    # Results
    # ==================================================

    st.divider()

    st.subheader("📊 Prediction Result")

    st.metric(
        "Probability of Diabetes",
        f"{probability*100:.2f}%"
    )

    if probability < 0.30:
        risk = "🟢 Low Risk"

    elif probability < 0.70:
        risk = "🟡 Moderate Risk"

    else:
        risk = "🔴 High Risk"

    st.markdown(f"## {risk}")

    if prediction == 1:

        st.error(
            "⚠️ The model predicts that the patient is likely to have Diabetes."
        )

    else:

        st.success(
            "✅ The model predicts that the patient is unlikely to have Diabetes."
        )

    # ==================================================
    # Recommendations
    # ==================================================

    st.markdown("---")

    st.subheader("💡 Health Recommendations")

    if prediction == 1:

        st.warning("""
- Consult a healthcare professional.
- Monitor your blood glucose regularly.
- Maintain a healthy and balanced diet.
- Exercise regularly.
- Follow your doctor's advice.
""")

    else:

        st.info("""
- Continue maintaining a healthy lifestyle.
- Eat a balanced diet.
- Exercise regularly.
- Stay physically active.
- Schedule regular health checkups.
""")

# ======================================================
# Footer
# ======================================================

st.markdown("---")

st.caption(
    "Built by Bhoomika Patle | Diabetes Prediction App using Streamlit & Scikit-learn"
)