import streamlit as st
import pandas as pd
import pdfkit
from srv.db.db import get_db

# Función para obtener fechas únicas
@st.cache_data
def obtener_fechas_unicas(_collection):
    return _collection.distinct('FECHA')

# Función para cargar datos según la fecha y tipo de reporte
def cargar_datos(_collection, fecha, tipo_reporte):
    return list(_collection.find({"FECHA": fecha, "TIPO_REPORTE": tipo_reporte}))

# Función para obtener datos con los filtros aplicados
def obtener_datos(_collection, fecha, tipo_reporte):
    return cargar_datos(_collection, fecha, tipo_reporte)

# Función para generar contenido HTML
def generar_html_contenido(df, tipo_reporte):
    tabla_html = df.to_html(index=False)
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #ffffff;
                color: #000000;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 10px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Reporte {tipo_reporte}</h1>
        {tabla_html}
    </body>
    </html>
    """

# Función para generar PDF
def generar_pdf(html_content):
    pdf = pdfkit.from_string(html_content, False)
    return pdf

# Función principal
def main():
    st.title("Generar Reportes en PDF")

    # Conectar a la base de datos
    db = get_db()
    collection = db["match_URU"]

    # Selector de reporte
    reporte = st.selectbox("Selecciona el reporte que deseas descargar:", ["Dashboard Match", "Dashboard Individual"])

    # Obtener fechas únicas para el selector
    fechas_disponibles = obtener_fechas_unicas(collection)

    # Selector de fecha utilizando un selectbox como en el Dashboard Match
    fecha_seleccionada = st.selectbox('Seleccionar un Match:', fechas_disponibles)

    # Definir el tipo de reporte
    tipo_reporte = "Dashboard Match" if reporte == "Dashboard Match" else "Dashboard Individual"

    # Mostrar los datos en el dashboard
    data = obtener_datos(collection, fecha_seleccionada, tipo_reporte)
    df = pd.DataFrame(data)
    st.write(df)

    # Botón para descargar el PDF
    if st.button("Descargar PDF"):
        html_content = generar_html_contenido(df, tipo_reporte)
        pdf = generar_pdf(html_content)
        st.download_button(
            label="Descargar PDF",
            data=pdf,
            file_name=f"reporte_{tipo_reporte}_{fecha_seleccionada}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
