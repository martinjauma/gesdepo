import streamlit as st
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from app.main import main_page
from app.reports.reports_page import reports_page
from app.settings import settings_page
from app.form import form_page


#comentar al
def main():
    st.set_page_config(page_title="GesDepo App", layout="wide")

    render_navbar()  # Renderiza la barra de navegación si tienes una

    selection = render_sidebar()  # Renderiza la barra lateral y selecciona la página

    if selection == "Inicio":
        main_page()
    elif selection == "Reportes":
        reports_page()
    elif selection == "Configuración":
        settings_page()
    elif selection == "Formulario":
        form_page()

if __name__ == "__main__":
    main()
