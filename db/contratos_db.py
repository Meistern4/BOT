from db.conexion import obtener_conexion

def insertar_contrato(datos):
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        insert_query = """
        INSERT INTO ventas.contratos (
            nombre, identificacion, correo, fecha_inicio, fecha_fin,
            objeto_contrato, valor_total, condiciones, observaciones
        ) VALUES (
            %(nombre)s, %(identificacion)s, %(correo)s, %(fecha_inicio)s, %(fecha_fin)s,
            %(objeto_contrato)s, %(valor_total)s, %(condiciones)s, %(observaciones)s
        );
        """
        cur.execute(insert_query, datos)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error insertando contrato:", e)
        return False
    

def buscar_contrato_id(no_cotizacion):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM ventas.contratos
            WHERE cotizacion = %s
        """, (no_cotizacion,))

        row = cursor.fetchone()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        if row:
            return dict(zip(colnames, row))
        return None

    except Exception as e:
        print(f"Error buscando Contrato: {e}")
        return None
