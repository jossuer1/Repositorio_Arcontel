import streamlit as st
import pandas as pd
from io import BytesIO


def mostrar_dashboard():
    st.title("📊 Sistema de Homologación de Equipos")

    st.divider()

    st.warning("⚠️ El archivo debe tener exactamente estas columnas y en este orden.")

    st.info("📌 Si el archivo no cumple con el formato, no será procesado.")

    st.subheader("📁 Formato del archivo Excel")

    st.markdown("""
    El archivo debe cumplir con la siguiente estructura:

    | Campo      | Descripción                              |
    |------------|------------------------------------------|
    | MES        | Mes de registro                          |
    | AÑO        | Año de registro                          |
    | NOMBRE     | Empresa importadora                      |
    | RUC        | RUC de la empresa                        |
    | MARCA      | Marca del dispositivo                    |
    | MODELO     | Modelo del equipo                        |
    | PROVINCIA  | Provincia donde se registra/importa      |
    | CANTÓN     | Cantón correspondiente a la provincia    |
    | DOBLE      | Indica si es doble SIM (SI/NO)           |
    | CANTIDAD   | Número de equipos                        |
    """)

    columnas = [
        "MES", "AÑO", "NOMBRE", "RUC", "MARCA",
        "MODELO", "PROVINCIA", "CANTÓN", "DOBLE", "CANTIDAD"
    ]

    df = pd.DataFrame(columns=columnas)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Plantilla")

    st.download_button(
        label="📥 Descargar plantilla Excel",
        data=output.getvalue(),
        file_name="plantilla_homologacion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


   


    