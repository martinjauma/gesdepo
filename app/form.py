import streamlit as st
from pymongo import MongoClient

# Conectar a la base de datos MongoDB
client = MongoClient("tu_conexion_a_mongodb")
db = client["nombre_de_tu_base_de_datos"]
collection = db["nombre_de_tu_coleccion"]

def form_page():
    st.title("Formulario")
    
    with st.form(key='formulario'):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        edad = st.number_input("Edad", min_value=0)
        submit_button = st.form_submit_button(label='Enviar')

    if submit_button:
        # Crear el documento para insertar en MongoDB
        documento = {
            "nombre": nombre,
            "email": email,
            "edad": edad
        }
        
        # Insertar el documento en la colección
        collection.insert_one(documento)
        st.success(f"Formulario enviado. Nombre: {nombre}, Email: {email}, Edad: {edad}")
