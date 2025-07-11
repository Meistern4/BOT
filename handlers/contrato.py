from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from db.cotizaciones_db import obtener_datos_cliente  # se reutiliza
from db.contratos_db import insertar_contrato, buscar_contrato_id
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
from db.conexion import obtener_conexion
import os
from docx import Document
from docx2pdf import convert

IDENTIFICACION_CONTRATO, DATOS_CONTRATO = 30, 31

async def iniciar_contrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Por favor envíame la identificación del cliente.")
    return IDENTIFICACION_CONTRATO

async def elegir_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await recibir_identificacion_contrato(update, context)

async def recibir_identificacion_contrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    identificacion = update.message.text.strip()
    cliente = obtener_datos_cliente(identificacion)
    if cliente:
        nombres, apellidos, correo = cliente
        context.user_data["cliente"] = {
            "nombre": f"{nombres} {apellidos}",
            "identificacion": identificacion,
            "correo": correo,
        }
        await update.message.reply_text(
            f"✅ Cliente encontrado:\nNombre: {nombres} {apellidos}\nCorreo: {correo}\n\n"
            "Ahora envíame los datos del contrato en formato:\nclave: valor\nclave: valor"
        )
        return DATOS_CONTRATO
    else:
        await update.message.reply_text("❌ No se encontró el cliente. Intenta de nuevo.")
        return IDENTIFICACION_CONTRATO

async def recibir_datos_contrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    datos = {}
    for linea in texto.split("\n"):
        if ":" in linea:
            k, v = linea.split(":", 1)
            datos[k.strip().lower()] = v.strip()

    cliente = context.user_data["cliente"]

    datos_db = {
        'nombre': cliente['nombre'],
        'identificacion': cliente['identificacion'],
        'correo': cliente['correo'],
        'fecha_inicio': datos.get('fecha_inicio'),
        'fecha_fin': datos.get('fecha_fin'),
        'objeto_contrato': datos.get('objeto_contrato'),
        'valor_total': float(datos.get('valor_total') or 0),
        'condiciones': datos.get('condiciones'),
        'observaciones': datos.get('observaciones'),
    }

    exito = insertar_contrato(datos_db)
    if exito:
        await update.message.reply_text("✅ Contrato guardado exitosamente.")
    else:
        await update.message.reply_text("❌ Hubo un error al guardar el contrato.")

    return ConversationHandler.END

async def buscar_contrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Por favor envíame la NO_CONTIZACION de la contratos a buscar:")
    return 32  # NUEVO ESTADO

async def mostrar_contrato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    no_cotizacion = update.message.text.strip()
    contratos = buscar_contrato_id(no_cotizacion)

    if contratos:
        texto = "\n".join(f"{k}: {v}" for k, v in contratos.items())
        await update.message.reply_text(f"✅ Contrato encontrado:\n\n{texto}")
    else:
        await update.message.reply_text("❌ No se encontró ningún contrato con esa NO. Cotizacion.")

    return ConversationHandler.END
