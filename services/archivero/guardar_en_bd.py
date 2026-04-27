from database.conexion import get_connection
from datetime import datetime

from services.archivero.crear_obtener import obtener_o_crear_canton
from services.archivero.crear_obtener import obtener_o_crear_dispositivo
from services.archivero.crear_obtener import obtener_o_crear_empresa
from services.archivero.crear_obtener import obtener_o_crear_id


def guardar_en_bd(df, id_usuario, nombre_archivo,id_tarea):
   
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Registrar carga
        cursor.execute("""
            INSERT INTO cargas (id_usuario, nombre_archivo, estado, fecha_subida,id_tarea)
            VALUES (%s, %s, %s, %s,%s)
            RETURNING id_carga
        """, (id_usuario, nombre_archivo, "PROCESADO", datetime.now(),id_tarea))

        id_carga = cursor.fetchone()[0]

        # 2. Normalizar columnas
        df.columns = [c.upper().strip() for c in df.columns]

        data_exportaciones = []

        for _, row in df.iterrows():

            # Empresa
            id_empresa = obtener_o_crear_empresa( cursor,row["NOMBRE"],row["RUC"])
            # Dispositivo
            id_dispositivo = obtener_o_crear_dispositivo(cursor,row["MODELO"],row["MARCA"])

            # Provincia 
            id_provincia = obtener_o_crear_id(
                cursor, "provincias", "nombre", row["PROVINCIA"], "id_provincia"
            )

            # Cantón (RELACIONADO CON PROVINCIA)
            id_canton = obtener_o_crear_canton(
                cursor, row["CANTÓN"], id_provincia
            )

            data_exportaciones.append((
                id_empresa,
                id_dispositivo,
                id_provincia,
                id_canton,
                id_carga,
                row["MES"],
                row["AÑO"],
                row["CANTIDAD"],
                True if str(row["DOBLE"]).upper() == "SI" else False,
                datetime.now()
            ))

        # Inserción masiva
        cursor.executemany("""
            INSERT INTO exportaciones (
                id_empresa, id_dispositivo, id_provincia, id_canton,
                id_carga, mes, anio, cantidad, doble_sim, fecha_creacion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data_exportaciones)

         # Actualizar tarea como PROCESADA
        if id_tarea:
          cursor.execute("""
           UPDATE tareas_reportes
           SET estado = 'PROCESADO',
           fecha_procesado = %s
           WHERE id_tarea = %s
        """, (datetime.now(), id_tarea))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()