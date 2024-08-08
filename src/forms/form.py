import streamlit as st
import pymongo
from datetime import datetime
import uuid
import pandas as pd
import os
from dotenv import load_dotenv


# Carga el archivo .env
load_dotenv()


# Conexión a MongoDB utilizando variables de entorno
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["gestDep_db_json"]
collection = db["gest_dep_ALTA"]

def generar_id():
    return str(uuid.uuid4())

def buscar_registros_por_apellido(apellido):
    return collection.find({"Apellido": apellido.capitalize()})

def editar_registro(id_unico, nuevo_apellido, nuevo_nombre):
    try:
        result = collection.update_one({"ID": id_unico}, {"$set": {"Apellido": nuevo_apellido.capitalize(), "Nombre": nuevo_nombre.capitalize()}})
        if result.modified_count > 0:
            st.success(f"Registro con ID {id_unico} actualizado correctamente.")
        else:
            st.warning(f"No se encontró ningún registro con ID {id_unico}")
    except Exception as e:
        st.error(f"Error al actualizar el registro: {e}")

def eliminar_registro(id_unico):
    try:
        result = collection.delete_one({"ID": id_unico})
        if result.deleted_count > 0:
            st.success(f"Registro con ID {id_unico} eliminado correctamente.")
        else:
            st.warning(f"No se encontró ningún registro con ID {id_unico}")
    except Exception as e:
        st.error(f"Error al eliminar el registro: {e}")

def cargar_todos_los_datos():
    return list(collection.find())

def main():
    st.logo("img/uruLogo.png")
    st.title("Sistema de Gestión de Registros")

    opcion = st.selectbox("Selecciona una opción:", ["ALTA", "EDICIÓN", "ELIMINAR"])

    if opcion == "ALTA":
        st.subheader("Formulario de Alta")
        campos_formulario = ["Apellido", "Nombre", "Edad", "Dirección", "Teléfono", "Email", "ALTURA"]

        with st.form(key='miForm', clear_on_submit=True):
            datos_formulario = {campo: st.text_input(campo) for campo in campos_formulario}
            submit_button = st.form_submit_button("Alta")

        if submit_button:
            if all(datos_formulario.values()):
                id_unico = generar_id()
                fecha_alta = datetime.now().strftime("%Y%m%d%H:%M")
                nuevo_registro = {"ID": id_unico, "FechaAlta": fecha_alta}
                nuevo_registro.update({campo: valor.capitalize() for campo, valor in datos_formulario.items()})
                try:
                    result = collection.insert_one(nuevo_registro)
                    st.success(f"Formulario enviado con éxito. ID del registro: {result.inserted_id}")
                    st.subheader("Nuevo Registro Agregado")
                    st.dataframe(pd.DataFrame([nuevo_registro]))
                    st.subheader("Todos los Registros en la Base de Datos")
                    st.dataframe(pd.DataFrame(cargar_todos_los_datos()))
                except Exception as e:
                    st.error(f"Error al insertar el registro: {e}")
            else:
                st.error("Por favor, complete todos los campos.")

    elif opcion == "EDICIÓN":
        st.subheader("Buscar y Editar Registros")
        apellido_buscar = st.text_input("Buscar por Apellido")
        if apellido_buscar:
            resultados = buscar_registros_por_apellido(apellido_buscar)
            registros = list(resultados)

            if registros:
                apellidos = [registro["Apellido"] for registro in registros]
                apellidos_buscar = st.selectbox("Seleccionar Apellido", options=apellidos)

                if apellidos_buscar:
                    registro_seleccionado = next((registro for registro in registros if registro["Apellido"] == apellidos_buscar), None)
                    id_seleccionado = registro_seleccionado["ID"]
                    nuevo_apellido = st.text_input("Nuevo Apellido", value=registro_seleccionado["Apellido"])
                    nuevo_nombre = st.text_input("Nuevo Nombre", value=registro_seleccionado["Nombre"])

                    if st.button("Editar"):
                        editar_registro(id_seleccionado, nuevo_apellido, nuevo_nombre)
            else:
                st.warning("No se encontraron registros con ese apellido.")

    elif opcion == "ELIMINAR":
        st.subheader("Buscar y Eliminar Registros")
        apellido_buscar = st.text_input("Buscar por Apellido")
        if apellido_buscar:
            resultados = buscar_registros_por_apellido(apellido_buscar)
            registros = list(resultados)

            if registros:
                apellidos = [registro["Apellido"] for registro in registros]
                apellidos_buscar = st.selectbox("Seleccionar Apellido", options=apellidos)

                if apellidos_buscar:
                    registro_seleccionado = next((registro for registro in registros if registro["Apellido"] == apellidos_buscar), None)
                    id_seleccionado = registro_seleccionado["ID"]

                    if st.button("Eliminar"):
                        eliminar_registro(id_seleccionado)
            else:
                st.warning("No se encontraron registros con ese apellido.")

    st.subheader("Todos los Registros en la Base de Datos")
    st.dataframe(pd.DataFrame(cargar_todos_los_datos()))
