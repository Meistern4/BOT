from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from db.empleados_db import insertar_empleado_en_db
from telegram import ReplyKeyboardMarkup


ELEGIR_DOCUMENTO, RECIBIR_DATOS = 40, 41

AREAS = {
    "rrhh": ["registrar_empleado"],
}

async def iniciar_empleado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones = [[doc] for doc in AREAS["rrhh"]]
    teclado = ReplyKeyboardMarkup(botones, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "📄 Por favor selecciona el tipo de documento:",
        reply_markup=teclado
    )
    return ELEGIR_DOCUMENTO

async def elegir_empleado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    documento = update.message.text.lower().strip()
    if documento not in AREAS["rrhh"]:
        await update.message.reply_text("❌ Documento no válido.")

        return ELEGIR_DOCUMENTO
    
# Guardar el documento en el contexto del usuario
    context.user_data["documento"] = documento

# Crear el mensaje de ejemplo con el formato requerido
    ejemplo = (
    "📄 Ahora envíame los datos en el siguiente formato:\n"
    "Identificacion: 1018492520\n"
    "Nombre: JOAN\n"
    "Apellidos: PEREZ\n"
    "Empleado: Sí\n"
    "Clasificacion: Operativo\n"
    "Celular: 3201234567\n"
    "Direccion: Calle 123\n"
    "Ciudad: Bogotá\n"
    "Departamento: Cundinamarca\n"
    "Banco: Bancolombia\n"
    "Numero_Cuenta: 1234567890\n"
    "ARL: Sura\n"
    "EPS: Sanitas\n"
    "Pension: Protección\n"
    "Cargo: Soldador\n"
    "Nomina: Mensual\n"
    "Sueldo: 2000000\n"
    "Auxilio_Transporte: 162000\n"
    "No_Prestacionales: 0\n"
    "Tipo_Contrato: Indefinido\n"
    "Grupo: Producción\n"
    "Cotizacion: Completa\n"
    "Pantalon: 32\n"
    "Camisa: M\n"
    "Botas: 41\n"
    "Inicio: 2024-01-15\n"
    "Finalizo: \n"
    "Estado: Activo\n"
    )

# Enviar el mensaje al usuario
    await update.message.reply_text(ejemplo)

# Cambiar al estado esperado para recibir los datos
    return RECIBIR_DATOS



async def recibir_datos_empleado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    datos = {}
    for linea in texto.split("\n"):
        if ":" in linea:
            k, v = linea.split(":", 1)
            datos[k.strip().lower()] = v.strip()

    exito = insertar_empleado_en_db(datos)
    if exito:
        await update.message.reply_text("✅ Tercero guardado correctamente.")
    else:
        await update.message.reply_text("❌ Ocurrió un error al guardar.")
    return ConversationHandler.END
