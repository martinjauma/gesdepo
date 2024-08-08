import streamlit as st
from streamlit_option_menu import option_menu

# Funciones de autenticación
def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.stop()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Navigation
with st.sidebar:
    st.sidebar.title("Navegación")
    
    if st.session_state.logged_in:
        # Menú con íconos
        selected = option_menu(
            menu_title=None,  # Deja el título vacío
            options=["Dashboard Data Base", "Dashboard Match", "Dashboard Individual", "Formulario", "Logout"],
            icons=["bar-chart", "calendar-event", "person", "file-text", "box-arrow-right"],  # Lista de íconos
            menu_icon="cast",  # Ícono del menú
            default_index=0,  # Índice de la opción seleccionada por defecto
            orientation="vertical",  # Mantén el menú en orientación vertical
        )
    else:
        st.sidebar.write("Por favor, inicia sesión")
        login()
        selected = None  # No selecciona nada si no está logueado

# Página principal
if st.session_state.logged_in:
    if selected == "Dashboard Data Base":
        import reports.dashboard_Data_Base as db
        db.main()  # Ejecuta la función main() del dashboard
    elif selected == "Dashboard Match":
        import reports.dashboard_match as dm
        dm.main()
    elif selected == "Dashboard Individual":
        import reports.dashboard_ind as di
        di.main()
    elif selected == "Formulario":
        import forms.form as form
        form.main()
    elif selected == "Logout":
        logout()
else:
    st.write("Debes iniciar sesión para ver el contenido.")
