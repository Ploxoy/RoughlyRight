import streamlit as st

st.title("📊 Data Visualization Dashboard")
st.write("Choose a topic to explore interactive visualizations.")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a topic:", ["Temperature", "Finance", "Traffic", "Health"])

if page == "Temperature":
    from pages import temperature
    temperature.show()
elif page == "Finance":
    from pages import finance
    finance.show()
elif page == "Traffic":
    from pages import traffic
    traffic.show()
elif page == "Health":
    from pages import health
    health.show()
