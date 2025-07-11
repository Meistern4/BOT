from db.conexion import obtener_conexion

def obtener_datos_cliente(identificacion):
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("""
            SELECT nombres_tercero, apellidos_tercero, correo_electronico_contacto_principal 
            FROM administrativos.tercero WHERE identificacion = %s
        """, (identificacion,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        return cliente  # None si no existe
    except Exception as e:
        print("Error DB:", e)
        return None

def insertar_cotizacion(datos):
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        insert_query = """
        INSERT INTO ventas.cotizaciones (
            no_cotizacion, nombre, identificacion, correo, fecha, marca, referencia,
            asesor_chasis, asesor_inducar, carroceria, tipo_carroceria,
            medidas_internas, medidas_externas, descrip_medidas, forro_interno,
            forro_externo, vigas, puente, piso, marco, parales, compuertas,
            puertas, color, guarda_polvos, adicional, descrip_adicional,
            anclaje, bomper, aseguramiento, mecanismo_cierre, impermeabilizacion,
            accesorios_acero, accesorios, observaciones, forma_pago, valor_total,
            subtotal, iva_19, fecha_cierre, largo_externo, ancho_externo,
            alto_externo, largo_internas, ancho_internas, alto_internas
        ) VALUES (
            %(no_cotizacion)s,%(nombre)s, %(identificacion)s, %(correo)s, %(fecha)s, %(marca)s, %(referencia)s,
            %(asesor_chasis)s, %(asesor_inducar)s, %(carroceria)s, %(tipo_carroceria)s,
            %(medidas_internas)s, %(medidas_externas)s, %(descrip_medidas)s, %(forro_interno)s,
            %(forro_externo)s, %(vigas)s, %(puente)s, %(piso)s, %(marco)s, %(parales)s, %(compuertas)s,
            %(puertas)s, %(color)s, %(guarda_polvos)s, %(adicional)s, %(descrip_adicional)s,
            %(anclaje)s, %(bomper)s, %(aseguramiento)s, %(mecanismo_cierre)s, %(impermeabilizacion)s,
            %(accesorios_acero)s, %(accesorios)s, %(observaciones)s, %(forma_pago)s, %(valor_total)s,
            %(subtotal)s, %(iva_19)s, %(fecha_cierre)s, %(largo_externo)s, %(ancho_externo)s,
            %(alto_externo)s, %(largo_internas)s, %(ancho_internas)s, %(alto_internas)s
        );
        """
        cur.execute(insert_query, datos)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error insertando cotización:", e)
        return False

def buscar_cotizacion_id(no_cotizacion):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM ventas.cotizaciones
            WHERE no_cotizacion = %s
        """, (no_cotizacion,))

        row = cursor.fetchone()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        if row:
            return dict(zip(colnames, row))
        return None

    except Exception as e:
        print(f"Error buscando Cotizacion: {e}")
        return None
