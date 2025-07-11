from db.conexion import obtener_conexion
from decimal import Decimal
from datetime import datetime
import logging

def insertar_empleado_en_db(datos):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        insert_query = """ 
            INSERT INTO administrativos.empleado (
                identificacion, nombre, apellidos, empleado, clasificacion, celular,
                direccion, ciudad, departamento, banco, numero_cuenta,
                arl, eps, pension, cargo, nomina, sueldo, auxilio_transporte,
                no_prestacionales, tipo_contrato, grupo, cotizacion,
                pantalon, camisa, botas, inicio, finalizo, estado
            ) VALUES (
                %(Identificacion)s, %(Nombre)s, %(Apellidos)s, %(Empleado)s, %(Clasificacion)s, %(Celular)s,
                %(Direccion)s, %(Ciudad)s, %(Departamento)s, %(Banco)s, %(Numero_Cuenta)s,
                %(ARL)s, %(EPS)s, %(Pension)s, %(Cargo)s, %(Nomina)s, %(Sueldo)s, %(Auxilio_Transporte)s,
                %(No_Prestacionales)s, %(Tipo_Contrato)s, %(Grupo)s, %(Cotizacion)s,
                %(Pantalon)s, %(Camisa)s, %(Botas)s, %(Inicio)s, %(Finalizo)s, %(Estado)s
            );
        """

        campos = [
            "Identificacion", "Nombre", "Apellidos", "Empleado", "Clasificacion", "Celular",
            "Direccion", "Ciudad", "Departamento", "Banco", "Numero_Cuenta",
            "ARL", "EPS", "Pension", "Cargo", "Nomina", "Sueldo", "Auxilio_Transporte",
            "No_Prestacionales", "Tipo_Contrato", "Grupo", "Cotizacion",
            "Pantalon", "Camisa", "Botas", "Inicio", "Finalizo", "Estado"
        ]

        for campo in campos:
            datos.setdefault(campo, None)

        # Convertir strings vacíos a None
        for k, v in datos.items():
            if isinstance(v, str) and v.strip() == "":
                datos[k] = None

        # Convertir campos numéricos
        for campo_decimal in ["Sueldo", "Auxilio_Transporte", "No_Prestacionales"]:
            if datos[campo_decimal] is not None:
                try:
                    datos[campo_decimal] = Decimal(datos[campo_decimal])
                except:
                    datos[campo_decimal] = Decimal(0)

        # Convertir campos fecha
        for campo_fecha in ["Inicio", "Finalizo"]:
            if datos[campo_fecha]:
                try:
                    datos[campo_fecha] = datetime.strptime(datos[campo_fecha], "%Y-%m-%d")
                except:
                    datos[campo_fecha] = None

        # Normalizar campo booleano
        datos["Empleado"] = str(datos.get("Empleado", "")).lower() in ("sí", "si", "true", "1", "yes")

        cursor.execute(insert_query, datos)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        logging.error(f"❌ Error al insertar empleado: {e}")
        return False
