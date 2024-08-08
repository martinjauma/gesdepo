import streamlit as st

def render_sidebar():
    return st.sidebar.radio("Navegación", ["Inicio", "Reportes", "Configuración", "Formulario"])
