import streamlit as st
from view.dashboard_view import mostrar_dashboard
from view.subida_view import mostrar_subida

from view.admin_operativo.reportes_view import  panel_admin_tareas
from view.reportes_view import mostrar_historial

def mostrar_menu(usuario, rol_usuario):

    st.sidebar.title("Sistema")
    st.sidebar.success(f"Usuario: {usuario['nombre']} ({rol_usuario})")

    # Opciones dinámicas según rol
    opciones = ["Inicio"]

    if rol_usuario == "usuario":
        opciones += ["Subir Reporte", "Mis Reportes"]

    elif rol_usuario == "admin_operativo":
        opciones += [ "Reportes"]

    elif rol_usuario == "admin_sistema":
        opciones += ["Usuarios"]

    opcion = st.sidebar.radio("Menú", opciones)

    # Navegación
    if opcion == "Inicio":
        mostrar_dashboard()

    elif opcion == "Subir Reporte":
        mostrar_subida()

    elif opcion == "Mis Reportes":
        mostrar_historial(usuario["id_usuario"])

    elif opcion == "Reportes":
        panel_admin_tareas(usuario["id_usuario"])

    elif opcion == "Usuarios":
        st.write("Gestión de usuarios")

    st.sidebar.divider()

    # 🚪 logout
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()