from models.usuarios import obtener_usuario_por_correo
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login(correo, password):
    usuario = obtener_usuario_por_correo(correo)
    
    if not usuario:
        return None

    if usuario["password_hash"] != hash_password(password):
        return None

    usuario.pop("password_hash", None)

    return {
        "id_usuario": usuario["id_usuario"],
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "id_rol": usuario["id_rol"],
        "rol": usuario.get("rol") or "sin_rol" 
    }