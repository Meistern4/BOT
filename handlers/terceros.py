from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from db.terceros_db import insertar_tercero_en_db, buscar_tercero_por_id
from telegram import ReplyKeyboardMarkup


ELEGIR_DOCUMENTO, RECIBIR_DATOS = 10, 11

AREAS = {
    "administrativo": ["registro_tercero"],
}

async def iniciar_tercero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones = [[doc] for doc in AREAS["administrativo"]]
    teclado = ReplyKeyboardMarkup(botones, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "📄 Por favor selecciona el tipo de documento:",
        reply_markup=teclado
    )
    return ELEGIR_DOCUMENTO

async def elegir_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    documento = update.message.text.lower().strip()
    if documento not in AREAS["administrativo"]:
        await update.message.reply_text("❌ Documento no válido.")
        return ELEGIR_DOCUMENTO

    context.user_data["documento"] = documento
    ejemplo = (
        "📄 Ahora envíame los datos en formato:\n"
        "identificacion: 1018492520\n"
        "digito_verificacion: 1\n"
        "codigo_sucursal: 001\n"
        "tipo_identificacion: CC\n"
        "tipo_persona: Jurídica\n"
        "razon_social: INDUCAR SAS\n"
        "nombres_tercero: JOAN\n"
        "apellidos_tercero: Pérez\n"
        "nombre_comercial: Carrocerías JP\n"
        "direccion: Calle 123\n"
        "codigo_pais: CO\n"
        "codigo_departamento_estado: 11\n"
        "codigo_ciudad: 11001\n"
        "indicativo_telefono_principal: 1\n"
        "telefono_principal: 3201234567\n"
        "extension_telefono_principal: \n"
        "tipo_regimen_iva: Responsable\n"
        "codigo_responsabilidad_fiscal: R-99\n"
        "codigo_postal: 110111\n"
        "nombres_contacto_principal: Carlos\n"
        "apellidos_contacto_principal: Mendoza\n"
        "indicativo_telefono_contacto_principal: 1\n"
        "telefono_contacto_principal: 3004567890\n"
        "extension_telefono_contacto_principal: \n"
        "correo_electronico_contacto_principal: contacto@inducar.com\n"
        "identificacion_cobrador: 555\n"
        "identificacion_vendedor: 777\n"
        "otros: Sin observaciones\n"
        "es_cliente: sí\n"
        "es_proveedor: no\n"
        "estado: activo\n"
    )
    await update.message.reply_text(ejemplo)
    return RECIBIR_DATOS


async def recibir_datos_tercero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    datos = {}
    for linea in texto.split("\n"):
        if ":" in linea:
            k, v = linea.split(":", 1)
            datos[k.strip().lower()] = v.strip()

    exito = insertar_tercero_en_db(datos)
    if exito:
        await update.message.reply_text("✅ Tercero guardado correctamente.")
    else:
        await update.message.reply_text("❌ Ocurrió un error al guardar.")
    return ConversationHandler.END



async def buscar_tercero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Por favor envíame la identificación del tercero a buscar:")
    return 12  # NUEVO ESTADO

async def mostrar_tercero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    identificacion = update.message.text.strip()
    tercero = buscar_tercero_por_id(identificacion)

    if tercero:
        texto = "\n".join(f"{k}: {v}" for k, v in tercero.items())
        await update.message.reply_text(f"✅ Tercero encontrado:\n\n{texto}")
    else:
        await update.message.reply_text("❌ No se encontró ningún tercero con esa identificación.")

    return ConversationHandler.END
