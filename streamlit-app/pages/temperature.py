import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_temperature_data

def show():
    st.title("🌡️ Temperature Trends")

    df = load_temperature_data()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Mean_Temperature"], mode='lines+markers', name="Temperature"))
    
    st.plotly_chart(fig)
