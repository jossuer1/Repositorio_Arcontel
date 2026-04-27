
from datetime import datetime



def obtener_o_crear_id(cursor, tabla, columna_nombre, valor, columna_id):
    """Busca un ID por nombre; si no existe, lo crea."""
    if not valor or str(valor).strip() == "":
        return None
        
    query_select = f"SELECT {columna_id} FROM {tabla} WHERE {columna_nombre} = %s"
    cursor.execute(query_select, (str(valor).strip(),))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        query_insert = f"INSERT INTO {tabla} ({columna_nombre}, fecha_creacion) VALUES (%s, %s) RETURNING {columna_id}"
        cursor.execute(query_insert, (str(valor).strip(), datetime.now()))
        return cursor.fetchone()[0]
    
def obtener_o_crear_canton(cursor, nombre_canton, id_provincia):
    if not nombre_canton or str(nombre_canton).strip() == "":
        return None

    nombre_canton = str(nombre_canton).strip()

    # Buscar cantón con su provincia
    cursor.execute("""
        SELECT id_canton
        FROM cantones
        WHERE nombre = %s AND id_provincia = %s
    """, (nombre_canton, id_provincia))

    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute("""
            INSERT INTO cantones (nombre, id_provincia, fecha_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_canton
        """, (nombre_canton, id_provincia, datetime.now()))

        return cursor.fetchone()[0]

def obtener_o_crear_empresa(cursor, nombre, ruc):
    if not ruc or str(ruc).strip() == "":
        raise ValueError("El RUC es obligatorio para registrar la empresa")

    nombre = str(nombre).strip() if nombre else None
    ruc = str(ruc).strip()

    # 1. Buscar por RUC
    cursor.execute("""
        SELECT id_empresa, nombre
        FROM empresas
        WHERE ruc = %s
    """, (ruc,))
    result = cursor.fetchone()

    if result:
        id_empresa, nombre_bd = result

        # 2. Si existe pero el nombre cambió, lo actualizamos
        if nombre and nombre_bd != nombre:
            cursor.execute("""
                UPDATE empresas
                SET nombre = %s
                WHERE id_empresa = %s
            """, (nombre, id_empresa))

        return id_empresa

    else:
        # 3. Crear nueva empresa
        cursor.execute("""
            INSERT INTO empresas (nombre, ruc, fecha_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_empresa
        """, (nombre, ruc, datetime.now()))

        return cursor.fetchone()[0]
    
def obtener_o_crear_dispositivo(cursor, modelo, marca):
    if not modelo or str(modelo).strip() == "":
        return None

    modelo = str(modelo).strip()
    marca = str(marca).strip() if marca else None

    # Buscar por modelo + marca
    cursor.execute("""
        SELECT id_dispositivo
        FROM dispositivos
        WHERE modelo = %s AND marca = %s
    """, (modelo, marca))

    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute("""
            INSERT INTO dispositivos (modelo, marca, fecha_creacion)
            VALUES (%s, %s, %s)
            RETURNING id_dispositivo
        """, (modelo, marca, datetime.now()))

        return cursor.fetchone()[0]
