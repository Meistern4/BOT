import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        dbname="Inducar",
        user="andresgalvis",
        password="",
        host="localhost",
        port=5432
    )
