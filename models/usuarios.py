from database.conexion import get_connection

def obtener_usuario_por_correo(correo):
    conn = get_connection()
    cursor = conn.cursor()

    query = """SELECT 
        u.id_usuario,
        u.nombre,
        u.correo,
        u.password_hash,
        u.id_rol,
        COALESCE(r.nombre, 'sin_rol') AS rol  -- Asegura que siempre haya un string
        FROM usuarios u
        LEFT JOIN roles r ON u.id_rol = r.id_rol -- LEFT JOIN es la clave
        WHERE u.correo = %s;
    """

    cursor.execute(query, (correo,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "id_usuario": row[0],
            "nombre": row[1],
            "correo": row[2],
            "password_hash": row[3],
            "id_rol": row[4],
            "rol": row[5]   
        }

    return None