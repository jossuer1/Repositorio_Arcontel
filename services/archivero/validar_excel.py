import streamlit as st
import pandas as pd

def validar_excel(df):
    errores = []

    # Columnas esperadas
    columnas_esperadas = [
        "MES", "AÑO", "NOMBRE", "RUC",
        "MARCA", "MODELO", "PROVINCIA",
        "CANTÓN", "DOBLE", "CANTIDAD"
    ]

    # 1. Validar columnas exactas
    if list(df.columns) != columnas_esperadas:
        errores.append("Las columnas no coinciden con el formato requerido.")

    # 2. Validar valores nulos
    if df.isnull().any().any():
        errores.append("Existen celdas vacías en el archivo.")

    # 3. Validar CANTIDAD numérica
    if not pd.api.types.is_numeric_dtype(df["CANTIDAD"]):
        errores.append("La columna CANTIDAD debe ser numérica.")

    # 4. Validar DOBLE (SI / NO)
    if not df["DOBLE"].isin(["SI", "NO"]).all():
        errores.append("La columna DOBLE solo puede contener SI o NO.")

    # 5. Validar AÑO numérico
    if not pd.api.types.is_numeric_dtype(df["AÑO"]):
        errores.append("La columna AÑO debe ser numérica.")

    return errores