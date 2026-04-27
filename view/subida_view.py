import streamlit as st
import pandas as pd
import time
from datetime import datetime

from database.conexion import get_connection
from services.archivero.validar_excel import validar_excel
from services.archivero.guardar_en_bd import guardar_en_bd


def mostrar_subida():
    # 1. Datos de sesión
    usuario_data = st.session_state.get("usuario", {})
    rol = usuario_data.get("rol")
    id_usuario = usuario_data.get("id_usuario")

    # 2. Control de acceso
    roles_permitidos = ["usuario", "admin_operativo", "admin_sistema"]
    if rol not in roles_permitidos:
        st.error("No autorizado para acceder a esta sección.")
        st.stop()

    st.title("Subir archivo Excel")

    # 3. Obtener tareas pendientes
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_tarea, descripcion, tipo_reporte, fecha_creacion
    FROM tareas_reportes
    WHERE id_usuario_asignado = %s
    AND estado = 'PENDIENTE'
    ORDER BY fecha_creacion DESC
     """, (id_usuario,))

    tareas = cursor.fetchall()

    # 4. Mostrar tabla o mensaje

    df_tareas = pd.DataFrame(tareas, columns=[
      "ID", "Descripción", "Tipo", "Fecha"
    ])

    if df_tareas.empty:
      st.info("📭 Sin actividades pendientes")
      return

    st.subheader("📋 Tareas asignadas")
    st.dataframe(df_tareas, use_container_width=True)

    # 5. Selección de tarea
    opciones = ["-- Selecciona una tarea --"] + df_tareas["ID"].tolist()

    id_tarea = st.selectbox(
      "Selecciona la tarea a resolver",
    opciones
    )

    # Evitar continuar si no ha elegido
    if id_tarea == "-- Selecciona una tarea --":
      st.warning("Selecciona una tarea para continuar")
      return

    # 6. Mostrar detalle
    tarea_info = df_tareas[df_tareas["ID"] == id_tarea].iloc[0]

    st.success(f"Trabajando en: {tarea_info['Descripción']} ({tarea_info['Tipo']})")
    # 5. Subida de archivo
    archivo = st.file_uploader(
        "Selecciona un archivo Excel",
        type=["xlsx"],
        key="uploader_excel"
    )

    if archivo:
        try:
            df = pd.read_excel(archivo)
            errores = validar_excel(df)

            if errores:
                st.error("El archivo no cumple con el formato requerido:")
                for e in errores:
                    st.write(f"- {e}")
                return

            st.success("Archivo validado correctamente")
            st.dataframe(df)

            st.warning("¿Confirmas que deseas procesar y guardar estos datos?")

            col1, col2 = st.columns(2)

            # 6. Confirmar procesamiento
            with col1:
                if st.button("Sí, procesar"):
                    try:
                        guardar_en_bd(
                            df,
                            id_usuario,
                            archivo.name,
                            id_tarea  
                        )

                        st.success("Datos Guardando ...Espere")

                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.03)
                            progress_bar.progress(i + 1)

                        st.success("Tarea completada correctamente")

                        # limpiar uploader
                        st.session_state.pop("uploader_excel", None)
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error al guardar en BD: {e}")

            # 7. Cancelar
            with col2:
                if st.button("Cancelar"):
                    st.session_state.pop("uploader_excel", None)
                    st.rerun()

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            st.info("Asegúrate de que el archivo no esté dañado o abierto.")