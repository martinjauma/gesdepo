import pandas as pd
import re

def procesar_datos(partidos):
    df = pd.DataFrame(partidos)
    if not df.empty:
        regex = r"(\d{6})-(\w{3})-P(\d{2})-(\w{3})@(\w{3})"
        
        def extraer_informacion_fecha(fecha):
            match = re.search(regex, fecha)
            if match:
                return match.groups()
            else:
                return [None] * 5

        df[['FECHA_EXTRAIDA', 'TORNEO', 'PARTIDO', 'LOCAL', 'VISITA']] = df['FECHA'].apply(
            lambda fecha: pd.Series(extraer_informacion_fecha(fecha))
        )

        def determinar_condicion(row):
            equipo, local, visita = row.get('EQUIPO', ''), row.get('LOCAL', ''), row.get('VISITA', '')
            if equipo == "01-URU" and local == "URU":
                return "LOCAL"
            elif equipo == "02-FRA" and visita == "FRA":
                return "VISITA"
            elif equipo == "03-ARG" and visita == "ARG":
                return "VISITA"
            elif equipo == "04-ESC" and visita == "ESC":
                return "VISITA"
            return "UNKNOWN"

        df['CONDICION'] = df.apply(determinar_condicion, axis=1)

        def calcular_puntaje(row, condicion):
            row_name, resultado = row.get('Row Name', ''), row.get('RESULTADO', '')
            if row_name == "TRY" and row['CONDICION'] == condicion:
                return 5
            elif row_name == "TRY PENAL" and row['CONDICION'] == condicion:
                return 7
            elif row_name == "GOAL" and resultado == "CONVERTIDO" and row['CONDICION'] == condicion:
                return 2
            elif row_name == "PENALTY KICK" and resultado == "CONVERTIDO" and row['CONDICION'] == condicion:
                return 3
            elif row_name == "DROP" and resultado == "CONVERTIDO" and row['CONDICION'] == condicion:
                return 3
            return 0

        df['SCORE LOCAL'] = df.apply(lambda row: calcular_puntaje(row, 'LOCAL'), axis=1)
        df['SCORE VISITA'] = df.apply(lambda row: calcular_puntaje(row, 'VISITA'), axis=1)
        
        return df
    return pd.DataFrame()
