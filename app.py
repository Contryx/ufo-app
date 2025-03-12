import streamlit as st


def set_background(image_url):
    """
    Adds a background image using CSS.
    :param image_url: URL or local path of the background image.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_background("https://images.nationalgeographic.org/image/upload/v1638892233/EducationHub/photos/crops-growing-in-thailand.jpg") 




import streamlit as st
import joblib
import pandas as pd

# Load trained pipeline
model = joblib.load("mlp_model.pkl")

# Custom CSS to style labels, reduce spacing, and add white boxes for warnings
st.markdown(
    """
    <style>
        /* Make title clear and readable */
        .title {
            color: black !important;
            font-size: 26px !important;
            font-weight: bold !important;
            text-align: center;
        }

        /* Improve label styling - keep bold and make the white box fit the text */
        .stNumberInput label, .stSelectbox label {
            font-size: 14px !important;
            font-weight: bold !important;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 2px 5px !important; /* Adjusted padding for better fit */
            border-radius: 3px !important; /* Smaller rounded corners */
            display: inline-block;
            margin-bottom: -2px !important; /* Reduce spacing between label and input */
        }

        /* Reduce gap between inputs */
        div[data-testid="stNumberInput"], div[data-testid="stSelectbox"] {
            margin-top: -2px !important; /* Pull input boxes closer to labels */
        }

        /* Improve button visibility */
        div.stButton > button {
            font-size: 18px !important;
            padding: 12px 24px;
            font-weight: bold !important;
            background-color: white !important;
            border-radius: 8px;
            border: none;
        }

        /* Style for prediction result box */
        .result-box {
            font-size: 20px !important;
            font-weight: bold !important;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-top: 15px;
            border: 2px solid black;
        }

        /* Style for warning message box */
        .warning-box {
            font-size: 16px !important;
            font-weight: bold !important;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid red;
            color: black !important;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Title (Without Emojis)
st.markdown('<h1 class="title">Crop Yield Prediction</h1>', unsafe_allow_html=True)

# User Inputs (Bold Labels, No Emojis)
average_rain_fall_mm_per_year = st.number_input("**Avg Rainfall (mm/year):**", min_value=0.0, value=0.0)
avg_temp = st.number_input("**Avg Temperature (°C):**", min_value=-10.0, value=0.0)
pesticides_tonnes = st.number_input("**Pesticides (tonnes):**", min_value=0.0, value=0.0)
area = st.selectbox("**Location:**", ["India", "Europe"])

# Include 'Item' selection
item_options = ["Maize", "Potatoes", "Rice, paddy", "Sorghum", "Wheat"]
item = st.selectbox("**Crop Type:**", item_options)

# Create input DataFrame
input_data = pd.DataFrame({
    'average_rain_fall_mm_per_year': [average_rain_fall_mm_per_year],
    'avg_temp': [avg_temp],
    'pesticides_tonnes': [pesticides_tonnes],
    'Area': [area],
    'Item': [item]  
})

# Prediction Button
if st.button("Predict Yield"):
    # Check if all numerical inputs are zero
    if average_rain_fall_mm_per_year == 0 and avg_temp == 0 and pesticides_tonnes == 0:
        st.markdown(
            '<div class="warning-box">⚠️ Please enter valid values for rainfall, temperature, and pesticides to get a prediction.</div>',
            unsafe_allow_html=True
        )
    else:
        try:
            predicted_yield = model.predict(input_data)[0]
            st.markdown(
                f'<div class="result-box"><b>Predicted Yield for {area} ({item}):</b> <br> <span style="font-size:22px;">{predicted_yield:.2f} hg/ha</span></div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error making prediction: {e}")

