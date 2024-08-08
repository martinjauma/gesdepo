import streamlit as st

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.experimental_rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.experimental_rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Navigation
st.sidebar.title("Navegación")

if st.session_state.logged_in:
    page = st.sidebar.radio("Selecciona una opción", ["Dashboard Data Base", "Dashboard Match", "Dashboard Individual", "Formulario", "Logout"])

    if page == "Dashboard Data Base":
        import reports.dashboard_Data_Base as db
        db.main()
    elif page == "Dashboard Match":
        import reports.dashboard_match as dm
        dm.main()
    elif page == "Dashboard Individual":
        import reports.dashboard_ind as di
        di.main()
    elif page == "Formulario":
        import forms.form as form
        form.main()
    elif page == "Logout":
        logout()
else:
    st.sidebar.write("Por favor, inicia sesión")
    login()
