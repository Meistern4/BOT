from db.conexion import obtener_conexion
def insertar_tercero_en_db(datos):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO administrativos.tercero (
                identificacion, digito_verificacion, codigo_sucursal, tipo_identificacion,
                tipo_persona, razon_social, nombres_tercero, apellidos_tercero, nombre_comercial,
                direccion, codigo_pais, codigo_departamento_estado, codigo_ciudad,
                indicativo_telefono_principal, telefono_principal, extension_telefono_principal,
                tipo_regimen_iva, codigo_responsabilidad_fiscal, codigo_postal,
                nombres_contacto_principal, apellidos_contacto_principal,
                indicativo_telefono_contacto_principal, telefono_contacto_principal,
                extension_telefono_contacto_principal, correo_electronico_contacto_principal,
                identificacion_cobrador, identificacion_vendedor, otros,
                es_cliente, es_proveedor, estado
            ) VALUES (
                %(identificacion)s, %(digito_verificacion)s, %(codigo_sucursal)s, %(tipo_identificacion)s,
                %(tipo_persona)s, %(razon_social)s, %(nombres_tercero)s, %(apellidos_tercero)s, %(nombre_comercial)s,
                %(direccion)s, %(codigo_pais)s, %(codigo_departamento_estado)s, %(codigo_ciudad)s,
                %(indicativo_telefono_principal)s, %(telefono_principal)s, %(extension_telefono_principal)s,
                %(tipo_regimen_iva)s, %(codigo_responsabilidad_fiscal)s, %(codigo_postal)s,
                %(nombres_contacto_principal)s, %(apellidos_contacto_principal)s,
                %(indicativo_telefono_contacto_principal)s, %(telefono_contacto_principal)s,
                %(extension_telefono_contacto_principal)s, %(correo_electronico_contacto_principal)s,
                %(identificacion_cobrador)s, %(identificacion_vendedor)s, %(otros)s,
                %(es_cliente)s, %(es_proveedor)s, %(estado)s
            );
        """

        campos = [
            "identificacion", "digito_verificacion", "codigo_sucursal", "tipo_identificacion",
            "tipo_persona", "razon_social", "nombres_tercero", "apellidos_tercero", "nombre_comercial",
            "direccion", "codigo_pais", "codigo_departamento_estado", "codigo_ciudad",
            "indicativo_telefono_principal", "telefono_principal", "extension_telefono_principal",
            "tipo_regimen_iva", "codigo_responsabilidad_fiscal", "codigo_postal",
            "nombres_contacto_principal", "apellidos_contacto_principal",
            "indicativo_telefono_contacto_principal", "telefono_contacto_principal",
            "extension_telefono_contacto_principal", "correo_electronico_contacto_principal",
            "identificacion_cobrador", "identificacion_vendedor", "otros",
            "es_cliente", "es_proveedor", "estado"
        ]

        for campo in campos:
            datos.setdefault(campo, None)

        datos["es_cliente"] = str(datos.get("es_cliente", "")).lower() in ("sí", "si", "true", "1", "yes")
        datos["es_proveedor"] = str(datos.get("es_proveedor", "")).lower() in ("sí", "si", "true", "1", "yes")

        cursor.execute(insert_query, datos)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error al insertar tercero: {e}")
        return False

def buscar_tercero_por_id(identificacion):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM administrativos.tercero
            WHERE identificacion = %s
        """, (identificacion,))

        row = cursor.fetchone()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        if row:
            return dict(zip(colnames, row))
        return None

    except Exception as e:
        print(f"Error buscando tercero: {e}")
        return None
