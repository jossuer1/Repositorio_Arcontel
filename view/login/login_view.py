import streamlit as st
from services.login.auth_service import login
from services.login.logueo_service import registrar_logueo
from services.archivero.device_service import obtener_ip, obtener_dispositivo

def mostrar_login():
    st.title("Sistema de Homologación")

    correo = st.text_input("Correo")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if not correo or not password:
            st.warning("Completa todos los campos")
            return

        usuario = login(correo, password)

        if usuario:
            #  Aseguramos que 'rol' existe o ponemos uno por defecto
            st.session_state["usuario"] = {
                "id_usuario": usuario.get("id_usuario"),
                "nombre": usuario.get("nombre"),
                "rol": usuario.get("rol", "sin_rol") 
            }

            st.session_state["logueado"] = True

            # auditoría
            registrar_logueo(
                usuario["id_usuario"],
                obtener_ip(),
                obtener_dispositivo()
            )
            
            st.rerun()
        else:
            st.error("Credenciales incorrectas")