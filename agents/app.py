import streamlit as st

st.title("✈️ Travel Planning Agent")

user_input = st.text_input(
    "Describe your trip",
    "Plan a 10-day trip to Japan in April under $3000 for 2 people"
)

if st.button("Generate Plan"):

    st.subheader("Suggested Travel Plan")

    st.write("✈️ Flight: Korean Air JFK → NRT ($1060)")
    st.write("🏨 Hotel: APA Hotel Asakusa ($1500)")
    st.write("💰 Total Cost: $2560 of $3000 budget")

    st.success("Plan generated using multi-agent workflow demo")
