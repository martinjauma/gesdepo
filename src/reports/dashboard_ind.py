import pandas as pd
import streamlit as st
from srv.db.db import get_db
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests

# URL base donde se almacenan las imágenes de los jugadores
URL_BASE_IMAGENES = 'https://storage.googleapis.com/slar2024/TEROS/FOTOS/'
# URL de la imagen predeterminada
URL_IMAGEN_DEFAULT = 'https://storage.googleapis.com/slar2024/TEROS/TEAMS_strea/uruLogo.png'

def obtener_url_imagen(nombre_jugador):
    url_imagen = f'{URL_BASE_IMAGENES}{nombre_jugador}.png'
    response = requests.get(url_imagen)
    if response.status_code == 200:
        return url_imagen
    else:
        return URL_IMAGEN_DEFAULT

def main():
    db = get_db()
    collection = db["ind_URU"]

    @st.cache_resource
    def cargar_todos_los_datos():
        return list(collection.find({}))

    datos = cargar_todos_los_datos()
    df = pd.DataFrame(datos)

    def renombrar_row_name(row_name):
        if row_name in [
            "P1 - Pase  Pos", "P2 - Pase Neg", "PL - Offload", "PM - Pelota  en mano",
            "PO - Recep  Aerea Pos", "PQ - Recep  Aerea Levantada", "PR - Perdidas",
            "PT + Pie Pos", "PT - Pie Neg", "Q9 - Maul  Ataque", "QP Presentacion Pos",
            "QP Presentacion +", "QP Presentacion -", "QP Presentacion NEG",
            "QR + 1o Ruck Ata POS", "QR + 2o Ruck Ata POS", "QR + 3o Ruck Ata POS",
            "QR - 1o Ruck Ata NEG", "QR - 2o Ruck Ata NEG", "QR - 3o Ruck Ata NEG"]:
            return "ACC ATAQUE"
        elif row_name in [
            "D1 - TA Pos", "D2 - Tackle", "D3 - TA Asist +", "D4 - TA Asist",
            "D5 - TA Off Load", "D6 - TA Err", "D7 - Pescada", "D8 - Recuperada",
            "D9 - Maul  Defensivo", "DC - Contest  Aereo +", "DC - Contest  Aereo -",
            "DR + 1o Ruck Def  POS", "DR + 2o Ruck Def  POS", "DR + 3o Ruck Def  POS",
            "DR - 1o Ruck Def  NEG", "DR - 2o Ruck Def  NEG", "DR - 3o Ruck Def  NEG"]:
            return "ACC DEFENSIVAS"
        elif row_name in [
            "R1 Penal", "R2 Duelo Gan", "R3 Duelo Emp", "R4 Duelo Per", "R5 Try",
            "R6 Conversion +", "R7 Conversion -", "S1 - Pase + Medio", "S2 - Pase - Medio",
            "S3 Patada +  Especialista", "S4 Patada - Especialista", "T1 Scrum +",
            "T1 Scrum -", "T2 Line +", "T2 Line -", "T3 Lanzamiento  Line +",
            "T3 Lanzamiento  Line -"]:
            return "ACC ESPECIALES"
        else:
            return "OTRO"

    df['Grupo Row Name'] = df['Row Name'].apply(renombrar_row_name)

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        fechas_disponibles = df['FECHA'].unique()
        fechas_seleccionadas = st.multiselect('Seleccionar una o varias fechas:', fechas_disponibles)
    
    with col2:
        nombres_disponibles = df['NOMBRE'].unique()
        nombre_seleccionado = st.selectbox('Seleccionar un nombre:', nombres_disponibles)

    if fechas_seleccionadas:
        df = df[df['FECHA'].isin(fechas_seleccionadas)]
    if nombre_seleccionado:
        df = df[df['NOMBRE'] == nombre_seleccionado]
        url_imagen_jugador = obtener_url_imagen(nombre_seleccionado)

    grupo_acc_atq = df[df['Grupo Row Name'] == 'ACC ATAQUE']
    grupo_acc_def = df[df['Grupo Row Name'] == 'ACC DEFENSIVAS']
    grupo_acc_esp = df[df['Grupo Row Name'] == 'ACC ESPECIALES']

    conteo_atq = grupo_acc_atq['Row Name'].value_counts().reset_index()
    conteo_atq.columns = ['ACC IND', 'Conteo']

    conteo_def = grupo_acc_def['Row Name'].value_counts().reset_index()
    conteo_def.columns = ['ACC IND', 'Conteo']

    conteo_esp = grupo_acc_esp['Row Name'].value_counts().reset_index()
    conteo_esp.columns = ['ACC IND', 'Conteo']

    def table_to_html(df):
        return df.to_html(index=False)

    def crear_grafico_radar(df, title):
        fig = px.line_polar(df, r='Conteo', theta='ACC IND', line_close=True, title=title)
        fig.update_traces(fill='toself', line=dict(color='rgba(78,169,200,0)'))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=False)
            ),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    def crear_grafico_radar_grupos(df, title):
        promedio_df = df.groupby('Grupo Row Name').size().reset_index(name='Conteo')
        promedio_df.columns = ['ACC IND', 'Conteo']
        
        fig = px.line_polar(promedio_df, r='Conteo', theta='ACC IND', line_close=True, title=title)
        fig.update_traces(fill='toself', line=dict(color='rgba(78,169,200,0)'))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=False),


            ),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    st.write('---')

    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        st.subheader('ACC ATAQUE')
        st.write(table_to_html(conteo_atq), unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: left; font-size: 24px;"><strong>Total ACC ATQ:</strong> {len(grupo_acc_atq)}</div>', unsafe_allow_html=True)

    with col2:
        st.subheader('ACC DEFENSIVAS')
        st.write(table_to_html(conteo_def), unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: left; font-size: 24px;"><strong>Total ACC DEF:</strong> {len(grupo_acc_def)}</div>', unsafe_allow_html=True)

    with col3:
        st.subheader('ACC ESPECIALES')
        st.write(table_to_html(conteo_esp), unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: left; font-size: 24px;"><strong>Total ACC ESP:</strong> {len(grupo_acc_esp)}</div>', unsafe_allow_html=True)

    with col4:
        if nombre_seleccionado:
            st.image(url_imagen_jugador, caption=f'{nombre_seleccionado}', use_column_width=True)

    st.write('---')

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader('ACC Seleccionadas')
        st.table(df['Grupo Row Name'].value_counts().reset_index().rename(columns={'index': 'ACC', 'Grupo Row Name': '#'}))

    with col2:
        st.plotly_chart(crear_grafico_radar_grupos(df, 'Gráfico de Radar Grupos'))

    
    col1, col2,col3 = st.columns(3)
    
    with col1:
     st.plotly_chart(crear_grafico_radar(conteo_atq, 'Gráfico de Radar ATAQUE'))
     
     with col2:
         st.plotly_chart(crear_grafico_radar(conteo_def, 'Gráfico de Radar DEFENSIVAS'))
     with col3:
         st.plotly_chart(crear_grafico_radar(conteo_esp, 'Gráfico de Radar ESPECIALES'))

if __name__ == "__main__":
    main()
