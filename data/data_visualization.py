import plotly.express as px
import streamlit as st

def crear_dona(data, titulo, valores, nombres):
    fig = px.pie(data, values=valores, names=nombres, hole=0.4, title=titulo)
    st.plotly_chart(fig)
