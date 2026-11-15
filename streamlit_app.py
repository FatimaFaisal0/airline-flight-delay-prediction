import streamlit as st

st.set_page_config(
    page_title="Flight Delay Prediction",
    page_icon="✈️"
)

st.title("✈️ Airline Flight Delay Prediction")

st.write("Enter your flight information.")

airline = st.text_input("Airline")
origin = st.text_input("Departure Airport")
destination = st.text_input("Destination Airport")

flight_date = st.date_input("Flight Date")
departure_time = st.time_input("Departure Time")

duration = st.number_input(
    "Scheduled Flight Duration (Minutes)",
    min_value=1,
    value=120
)

if st.button("Predict Flight Delay"):
    st.info("The machine learning model is not connected yet.")
