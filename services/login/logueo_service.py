from database.conexion import get_connection

def registrar_logueo(id_usuario, ip, dispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO logueo (id_usuario, ip_dispositivo, dispositivo)
        VALUES (%s, %s, %s)
    """, (id_usuario, ip, dispositivo))

    conn.commit()
    cursor.close()
    conn.close()