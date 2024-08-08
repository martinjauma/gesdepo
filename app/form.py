import streamlit as st
from app.database import get_database

def form_page():
    st.title("Formulario")
    db = get_database()
    collection = db['nombre_de_la_colección']

    # Campos del formulario (asegúrate de que coincidan con los de gduru)
    name = st.text_input("Nombre")
    age = st.number_input("Edad", min_value=0, max_value=100)
    position = st.text_input("Posición")  # Ejemplo de campo adicional

    if st.button("Enviar"):
        collection.insert_one({"name": name, "age": age, "position": position})
        st.success("Datos guardados exitosamente.")
