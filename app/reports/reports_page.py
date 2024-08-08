import streamlit as st
from app.reports.dashboard_Data_Base import dashboard_data_base
from app.reports.dashboard_match import dashboard_match
from app.reports.dashboard_ind import dashboard_ind

def reports_page():
    st.title("Reportes")
    report_selection = st.sidebar.radio("Selecciona un reporte", ["Base de Datos", "Match", "Individual"])

    if report_selection == "Base de Datos":
        dashboard_data_base()
    elif report_selection == "Match":
        dashboard_match()
    elif report_selection == "Individual":
        dashboard_ind()
