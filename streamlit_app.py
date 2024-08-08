import streamlit as st
from app.main import main_page
from app.reports import reports_page
from app.settings import settings_page
from app.form import form_page

def main():
    # Configura la página en Streamlit
    st.set_page_config(page_title="GDURU App", layout="wide")

    # Configura la barra lateral para navegación
    selection = st.sidebar.selectbox("Navegación", ["Inicio", "Reportes", "Configuración", "Formulario"])

    # Muestra el contenido basado en la selección
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


