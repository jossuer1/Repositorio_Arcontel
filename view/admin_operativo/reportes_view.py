import streamlit as st
import time 

from database.conexion import get_connection
from datetime import datetime

import pandas as pd


def panel_admin_tareas(id_admin):

    st.title("📋 Asignación de Reportes")

    conn = get_connection()
    cursor = conn.cursor()

    # Obtener usuarios (excepto el admin)
    cursor.execute("""
        SELECT id_usuario, nombre
        FROM usuarios
        WHERE id_rol = 1
    """, (id_admin,))
    
    usuarios = cursor.fetchall()

    if not usuarios:
        st.warning("No hay usuarios disponibles")
        return

    # Convertir a diccionario para selectbox
    usuarios_dict = {nombre: id for id, nombre in usuarios}

    # Formulario
    with st.form("form_asignar_tarea"):

        usuario_nombre = st.selectbox("Asignar a usuario", list(usuarios_dict.keys()))
        descripcion = st.text_area("Descripción del reporte")
        tipo = st.selectbox("Tipo de reporte", ["Mensual", "Equipos", "General"])

        submitted = st.form_submit_button("Asignar tarea")

        if submitted:
            try:
                cursor.execute("""
                    INSERT INTO tareas_reportes (
                        id_usuario_asignado,
                        id_usuario_creador,
                        descripcion,
                        tipo_reporte,
                        estado,
                        fecha_creacion
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    usuarios_dict[usuario_nombre],
                    id_admin,
                    descripcion,
                    tipo,
                    "PENDIENTE",
                    datetime.now()
                ))

                conn.commit()
                
                st.success("Tarea asignada correctamente")
                
                progress_bar = st.progress(0)

                for i in range(100):
                    time.sleep(0.02) 
                    progress_bar.progress(i + 1)
                
                st.rerun()
                
            except Exception as e:
                conn.rollback()
                st.error(f"Error: {e}")

    st.divider()
    # Filtro
    filtro = st.selectbox(
    "Filtrar por estado",
    ["Todos", "PENDIENTE", "PROCESADO"]
    )
    # Query base 
    query = """
    SELECT 
    u.nombre,
    t.descripcion,
    t.tipo_reporte,
    t.estado,
    t.fecha_creacion,
    t.fecha_procesado,
    c.nombre_archivo
    FROM tareas_reportes t
    JOIN usuarios u ON t.id_usuario_asignado = u.id_usuario
    LEFT JOIN cargas c ON t.id_tarea = c.id_tarea
    """
    # Aplicar filtro
    if filtro != "Todos":
        query += " WHERE t.estado = %s"

    # Orden siempre al final
    
    query += " ORDER BY t.fecha_creacion DESC"

    # Ejecutar
    if filtro != "Todos":
        cursor.execute(query, (filtro,))
    else:
        cursor.execute(query)
        
    # Obtener datos
    tareas = cursor.fetchall()

    # Mostrar
    if not tareas:
       st.info("No hay tareas para mostrar")
    else:
        df = pd.DataFrame(tareas, columns=[
        "Usuario", "Descripción", "Tipo",
        "Estado", "Fecha creación", "Fecha procesado", "Archivo"
        ])
        df["Archivo"] = df["Archivo"].fillna("Sin archivo")
        st.dataframe(df, use_container_width=True)