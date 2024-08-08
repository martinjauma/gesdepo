import streamlit as st

# Manejo de estado de sesión para el inicio de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.experimental_rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# Definir las páginas y sus rutas
def main():
    if st.session_state.logged_in:
        # Configurar la navegación
        pages = {
            "Account": [login_page, logout_page],
            "Reports": [dashboard_base_data, dashboard_match, dashboard_ind],
            "Form": [form]
        }
    else:
        pages = [login_page]

    pg = st.sidebar.radio("Menu", list(pages.keys()), index=0)

    if pg == "Account":
        st.sidebar.selectbox("Account Options", options=[login_page, logout_page])
    elif pg == "Reports":
        page = st.sidebar.selectbox("Reports", options=[dashboard_base_data, dashboard_match, dashboard_ind])
        st.experimental_rerun()
    elif pg == "Form":
        page = st.sidebar.selectbox("Form", options=[form])
        st.experimental_rerun()

# Crear las páginas
login_page = st.pages.Page(login, title="Log in", icon=":material/login:")
logout_page = st.pages.Page(logout, title="Log out", icon=":material/logout:")
dashboard_base_data = st.pages.Page("reports/dashboard_Data_Base.py", title="Dashboard Data Base", icon=":material/dashboard:", default=True)
dashboard_match = st.pages.Page("reports/dashboard_match.py", title="Dashboard Match", icon=":material/dashboard:", default=False)
dashboard_ind = st.pages.Page("reports/dashboard_ind.py", title="Dashboard Individual", icon=":material/dashboard:", default=False)
form = st.pages.Page("forms/1_Form.py", title="Formularios", icon=":material/bug_report:")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
