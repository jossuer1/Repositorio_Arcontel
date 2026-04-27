from view.login.login_view import mostrar_login
from view.menu import mostrar_menu

import streamlit as st

if "logueado" not in st.session_state:
    st.session_state["logueado"] = False

# LOGIN
if not st.session_state["logueado"]:
    mostrar_login()
    st.stop()

# APP
usuario = st.session_state["usuario"]
rol_usuario = usuario.get("rol", "sin_rol")

#MENU SEGUN ROL
mostrar_menu(usuario,rol_usuario)


