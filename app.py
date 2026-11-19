import streamlit as st
import pandas as pd
import joblib
import time

from input_validation import has_valid_required_measurements


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# LOAD MODEL
# ==========================================================

@st.cache_resource
def load_model():
    model = joblib.load("models/random_forest_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return model, scaler


model, scaler = load_model()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image("https://img.icons8.com/color/96/stethoscope.png", width=80)

    st.title("Diabetes Prediction")

    st.markdown("---")

    st.subheader("About")

    st.write("""
    This application predicts the likelihood of diabetes
    using a Machine Learning model trained on the
    Pima Indians Diabetes Dataset.
    """)

    st.markdown("---")

    st.subheader("Model Details")

    st.write("**Algorithm:** Random Forest")
    st.write("**Accuracy:** 77.92%")
    st.write("**Dataset:** Pima Indians Diabetes")
    st.write("**Features Used:** 8")

    st.markdown("---")

    st.subheader("Project")

    st.write("👩‍💻 Developed by")
    st.success("**Bhoomika Patle**")
    st.caption("Machine Learning Project")

    st.markdown("---")

    st.info("""
    **Note**

    This application is intended for educational purposes
    only and should not replace professional medical advice.
    """)


# ==========================================================
# MAIN HEADER
# ==========================================================

st.title("🩺 Diabetes Prediction App")

st.markdown("""
Welcome to the **Diabetes Prediction App**.

This application uses a **Machine Learning Random Forest model**
to estimate the likelihood of diabetes based on patient health information.

Please enter the patient's details below and click **Predict Diabetes**.
""")

st.markdown("---")


# ==========================================================
# FEATURE INFORMATION
# ==========================================================

with st.expander("📖 About the Input Features"):

    st.markdown("""
    ### Explanation of each input

    **Pregnancies**
    - Number of times the patient has been pregnant.

    **Glucose**
    - Plasma glucose concentration after a glucose tolerance test.

    **Blood Pressure**
    - Diastolic blood pressure (mm Hg).

    **Skin Thickness**
    - Triceps skin fold thickness (mm).

    **Insulin**
    - 2-Hour serum insulin (mu U/ml).

    **BMI**
    - Body Mass Index.

    **Diabetes Pedigree Function**
    - Indicates hereditary likelihood of diabetes.

    **Age**
    - Age of the patient in years.
    """)


# ==========================================================
# PATIENT INFORMATION
# ==========================================================

st.subheader("📋 Patient Information")

col1, col2 = st.columns(2)

with col1:

    pregnancies = st.number_input(
        "Pregnancies", min_value=0, max_value=20, value=1, step=1
    )

    glucose = st.number_input(
        "Glucose (mg/dL)", min_value=0, max_value=300, value=120
    )

    blood_pressure = st.number_input(
        "Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70
    )

    skin_thickness = st.number_input(
        "Skin Thickness (mm)", min_value=0, max_value=100, value=20
    )

with col2:

    insulin = st.number_input(
        "Insulin (mu U/ml)", min_value=0, max_value=900, value=80
    )

    bmi = st.number_input(
        "BMI", min_value=0.0, max_value=70.0, value=25.0, format="%.1f"
    )

    diabetes_pedigree = st.number_input(
        "Diabetes Pedigree Function",
        min_value=0.000,
        max_value=3.000,
        value=0.500,
        format="%.3f",
    )

    age = st.number_input(
        "Age", min_value=1, max_value=120, value=30
    )

st.markdown("---")


# ==========================================================
# INPUT WARNINGS
# ==========================================================

warnings = []

if glucose == 0:
    warnings.append("⚠️ Glucose should normally be greater than 0.")

if blood_pressure == 0:
    warnings.append("⚠️ Blood Pressure should normally be greater than 0.")

if skin_thickness == 0:
    warnings.append("⚠️ Skin Thickness should normally be greater than 0.")

if insulin == 0:
    warnings.append("⚠️ Insulin value should normally be greater than 0.")

if bmi == 0:
    warnings.append("⚠️ BMI should normally be greater than 0.")

for warning in warnings:
    st.warning(warning)


# ==========================================================
# BUTTONS
# ==========================================================

button_col1, button_col2 = st.columns(2)

with button_col1:

    predict_button = st.button(
        "🔍 Predict Diabetes",
        use_container_width=True,
        type="primary"
    )

with button_col2:

    if st.button("🔄 Reset Values", use_container_width=True):
        st.rerun()


# ==========================================================
# PREDICTION
# ==========================================================

if predict_button:

    if not has_valid_required_measurements(
        glucose, bmi, blood_pressure
    ):
        st.error(
            "Please enter valid Glucose, BMI, and Blood Pressure values."
        )
        st.stop()

    with st.spinner("Analyzing patient data..."):

        time.sleep(1)

        input_data = pd.DataFrame({
            "Pregnancies": [pregnancies],
            "Glucose": [glucose],
            "BloodPressure": [blood_pressure],
            "SkinThickness": [skin_thickness],
            "Insulin": [insulin],
            "BMI": [bmi],
            "DiabetesPedigreeFunction": [diabetes_pedigree],
            "Age": [age],
        })

        input_scaled = scaler.transform(input_data)

        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]


    # ==========================================================
    # PREDICTION RESULT
    # ==========================================================

    st.markdown("---")
    st.subheader("📊 Prediction Result")

    metric1, metric2 = st.columns(2)

    with metric1:
        st.metric(
            "Model Probability",
            f"{probability * 100:.2f}%"
        )

    with metric2:

        if probability < 0.30:
            risk = "🟢 Low"
        elif probability < 0.70:
            risk = "🟡 Moderate"
        else:
            risk = "🔴 High"

        st.metric("Model Risk Category", risk)

    st.progress(float(probability))

    st.caption("Model-estimated probability of the positive class.")

    if prediction == 1:

        st.error("The model predicts a positive diabetes outcome.")

    else:

        st.success("The model predicts a negative diabetes outcome.")

    st.info(
        "This result is generated by a machine learning model. "
        "It is not a medical diagnosis, and the probability should not "
        "be interpreted as clinical certainty."
    )


    # ==========================================================
    # HEALTH RECOMMENDATIONS
    # ==========================================================

    st.markdown("---")
    st.subheader("💡 Health Recommendations")

    if prediction == 1:

        st.warning("""
        ### Recommended Next Steps

        • Consult a healthcare professional.

        • Monitor blood glucose regularly.

        • Follow a healthy, balanced diet.

        • Exercise consistently.

        • Maintain a healthy body weight.

        • Follow your doctor's advice and schedule regular checkups.
        """)

    else:

        st.info("""
        ### Healthy Lifestyle Tips

        • Continue eating a balanced diet.

        • Stay physically active.

        • Maintain a healthy weight.

        • Drink enough water.

        • Get regular health checkups.

        • Continue your healthy lifestyle.
        """)


    # ==========================================================
    # DISCLAIMER
    # ==========================================================

    st.markdown("---")
    st.subheader("ℹ️ Disclaimer")

    st.caption("""
    This prediction is generated using a Machine Learning model and is intended
    for educational purposes only.

    It should **not** be considered a medical diagnosis.

    Always consult a qualified healthcare professional for medical advice.
    """)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model", "Random Forest")

with col2:
    st.metric("Accuracy", "77.92%")

with col3:
    st.metric("Features", "8")

st.markdown(
    "<center><h5>🩺 Built by <b>Bhoomika Patle</b></h5></center>",
    unsafe_allow_html=True,
)

st.caption(
    "Diabetes Prediction App | Machine Learning Project using Streamlit, Scikit-learn, Pandas & NumPy"
)