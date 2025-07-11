import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
)
from handlers.contrato import (
    iniciar_contrato, recibir_identificacion_contrato, recibir_datos_contrato, mostrar_contrato, buscar_contrato
)

from handlers.terceros import (
    iniciar_tercero, elegir_documento, recibir_datos_tercero, buscar_tercero, mostrar_tercero
)


from handlers.cotizaciones import (
    iniciar_cotizacion, recibir_identificacion, recibir_datos_cotizacion, buscar_cotizacion, mostrar_cotizacion, cotizacion_pdf, generar_pdf
)

from handlers.empleados import (
    iniciar_empleado, elegir_empleado, recibir_datos_empleado
)





# Importa aquí tus otros handlers para tareas nuevas cuando las crees
# from handlers.contratos import crear_contrato
# ...

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ELEGIR_AREA, ELEGIR_TAREA = range(2)


TERCEROS_ESTADOS = {
    "ELEGIR_DOCUMENTO": 10,
    "RECIBIR_DATOS": 11,
    "BUSCAR_TERCERO": 12  # NUEVO ESTADO
}


COTIZACIONES_ESTADOS = {
    "IDENTIFICACION": 20,
    "DATOS_COTIZACION": 21,
    "BUSCAR_COTIZACION": 22,  # NUEVO ESTADO
    "COTIZACION_PDF": 23

}
CONTRATOS_ESTADOS = {
    "IDENTIFICACION": 30,
    "DATOS_CONTRATO": 31,
    "BUSCAR_CONTRATO": 32  # NUEVO ESTADO
}

EMPLEADOS_ESTADOS = {
    "ELEGIR_DOCUMENTO": 40,
    "RECIBIR_DATOS": 41,
    "BUSCAR_EMPLEADO": 42  # NUEVO ESTADO
}



AREAS = {
    "administrativo": ["registro_tercero", "buscar_tercero"],
    "ventas": ["crear_cotizacion", "buscar_cotizacion","buscar_contrato", "cotizacion_pdf", "crear_contrato"],
    "produccion": ["crear_orden", "orden_compra"],
    "rrhh": ["registrar_empleado", "procesar_nomina"],
    "financiero": ["generar_reportes", "extractos"]
}

# Mapea las tareas a sus funciones manejadoras
TASK_HANDLERS = {
    "registro_tercero": iniciar_tercero,
    "buscar_tercero": buscar_tercero,
    "crear_cotizacion": iniciar_cotizacion,
    "buscar_cotizacion": buscar_cotizacion,
    "buscar_cotizacion": buscar_cotizacion,
    "cotizacion_pdf": cotizacion_pdf,
    "crear_contrato": iniciar_contrato,
    "buscar_contrato": buscar_contrato,
    "registrar_empleado": iniciar_empleado,


    

    # "crear_contrato": crear_contrato,  # Descomenta cuando crees la función
    # Añade las demás funciones aquí cuando las implementes
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Usuario inició conversación")
    areas_disponibles = list(AREAS.keys())
    teclado = ReplyKeyboardMarkup([[area] for area in areas_disponibles], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Bienvenido. Por favor selecciona el área:",
        reply_markup=teclado
    )
    return ELEGIR_AREA

async def elegir_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    area = update.message.text.lower().strip()
    if area not in AREAS:
        await update.message.reply_text("❌ Área no válida, intenta de nuevo.")
        return ELEGIR_AREA

    context.user_data["area"] = area
    tareas = AREAS[area]
    if not tareas:
        await update.message.reply_text("⚠️ No hay tareas configuradas para esta área.")
        return ConversationHandler.END

    teclado = ReplyKeyboardMarkup([[tarea] for tarea in tareas], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        f"Área seleccionada: {area}. Ahora selecciona la tarea:",
        reply_markup=teclado
    )
    return ELEGIR_TAREA

async def elegir_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tarea = update.message.text.lower().strip()
    area = context.user_data.get("area")

    if tarea not in AREAS.get(area, []):
        await update.message.reply_text("❌ Tarea no válida, intenta de nuevo.")
        return ELEGIR_TAREA

    context.user_data["tarea"] = tarea
    logger.info(f"Tarea seleccionada: {tarea} en el área {area}")

    handler_func = TASK_HANDLERS.get(tarea)
    if handler_func:
        await update.message.reply_text("✅ Iniciando tarea...", reply_markup=ReplyKeyboardRemove())
        return await handler_func(update, context)

    await update.message.reply_text("🚧 Esta tarea aún no está implementada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operación cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

router_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        ELEGIR_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_area)],
        ELEGIR_TAREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_tarea)],

        # Terceros
        TERCEROS_ESTADOS["ELEGIR_DOCUMENTO"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_documento)],
        TERCEROS_ESTADOS["RECIBIR_DATOS"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos_tercero)],
        TERCEROS_ESTADOS["BUSCAR_TERCERO"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_tercero)],

        # Cotizaciones
        COTIZACIONES_ESTADOS["IDENTIFICACION"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_identificacion)],
        COTIZACIONES_ESTADOS["DATOS_COTIZACION"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos_cotizacion)],
        COTIZACIONES_ESTADOS["BUSCAR_COTIZACION"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_cotizacion)],
        COTIZACIONES_ESTADOS["COTIZACION_PDF"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, generar_pdf)],


        # Contratos
        CONTRATOS_ESTADOS["IDENTIFICACION"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_identificacion_contrato)],
        CONTRATOS_ESTADOS["DATOS_CONTRATO"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos_contrato)],
        CONTRATOS_ESTADOS["BUSCAR_CONTRATO"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, mostrar_contrato)],


        # Empleados
        EMPLEADOS_ESTADOS["ELEGIR_DOCUMENTO"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, elegir_empleado)],
        EMPLEADOS_ESTADOS["RECIBIR_DATOS"]: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos_empleado)],

    },
    fallbacks=[CommandHandler("cancelar", cancelar)],
    allow_reentry=True
)
