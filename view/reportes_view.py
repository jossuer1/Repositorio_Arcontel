import streamlit as st
import pandas as pd
from database.conexion import get_connection


def mostrar_historial(id_usuario):

    st.title("📊 Mi Historial de Reportes")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        t.id_tarea,
        u_asignado.nombre AS usuario,
        u_creador.nombre AS solicitado_por,
        t.descripcion,
        t.tipo_reporte,
        t.estado,
        t.fecha_creacion,
        t.fecha_procesado,
        c.nombre_archivo,
        c.fecha_subida
    FROM tareas_reportes t
    JOIN usuarios u_asignado 
        ON t.id_usuario_asignado = u_asignado.id_usuario
    JOIN usuarios u_creador 
        ON t.id_usuario_creador = u_creador.id_usuario
    LEFT JOIN cargas c 
        ON t.id_tarea = c.id_tarea
    WHERE t.id_usuario_asignado = %s
    ORDER BY t.fecha_creacion DESC
    """, (id_usuario,))

    datos = cursor.fetchall()

    df = pd.DataFrame(datos, columns=[
        "ID",
        "Usuario",
        "Solicitado por",
        "Descripción",
        "Tipo",
        "Estado",
        "Fecha solicitud",
        "Fecha procesado",
        "Archivo",
        "Fecha subida"
    ])

    if df.empty:
        st.info("📭 No tienes historial todavía")
    else:
        df["Archivo"] = df["Archivo"].fillna("Sin archivo")
        df["Fecha procesado"] = df["Fecha procesado"].fillna("Pendiente")
        df["Fecha subida"] = df["Fecha subida"].fillna("No subido")

        st.dataframe(df, use_container_width=True)

    cursor.close()
    conn.close()