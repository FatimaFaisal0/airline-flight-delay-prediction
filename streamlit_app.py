import streamlit as st
import pandas as pd
import joblib

from datetime import date, time
from pathlib import Path

st.set_page_config(
    page_title="Flight Delay Prediction",
    page_icon="✈️"
)

@st.cache_resource
def load_model():
    return joblib.load(
        Path(__file__).parent / "flight_delay_model.pkl"
    )

model = load_model()

st.title("✈️ Airline Flight Delay Prediction")
st.write("Enter your flight information.")

encoder = model.named_steps["preprocessor"].named_transformers_["categorical"]

airline = st.selectbox("Airline", encoder.categories_[0])
origin = st.selectbox("Departure Airport", encoder.categories_[1])
destination = st.selectbox("Destination Airport", encoder.categories_[2])

flight_date = st.date_input(
    "Flight Date", date(2026, 1, 25)
)

departure_time = st.time_input(
    "Scheduled Departure Time", time(7, 0)
)

arrival_time = st.time_input(
    "Scheduled Arrival Time", time(10, 21)
)

duration = st.number_input(
    "Scheduled Flight Duration (Minutes)",
    min_value=1,
    value=381
)

distance = st.number_input(
    "Distance (Miles)",
    min_value=1,
    value=2475
)

if st.button("Predict Flight Delay"):

    if origin == destination:
        st.error("Please select different airports.")
        st.stop()

    input_data = pd.DataFrame([{
        "DAY_OF_MONTH": flight_date.day,
        "DAY_OF_WEEK": flight_date.weekday() + 1,
        "OP_UNIQUE_CARRIER": airline,
        "ORIGIN": origin,
        "DEST": destination,
        "CRS_DEP_TIME": departure_time.hour * 100 + departure_time.minute,
        "CRS_ARR_TIME": arrival_time.hour * 100 + arrival_time.minute,
        "CRS_ELAPSED_TIME": duration,
        "DISTANCE": distance,
        "DEP_HOUR": departure_time.hour
    }])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ Flight is likely to be delayed.")
    else:
        st.success("✅ Flight is likely not to be delayed.")

st.caption(
    "Random Forest model trained on January 2026 US flight data. "
    "Test accuracy: 60.31%. Predictions for other months "
    "have not been validated."
)
