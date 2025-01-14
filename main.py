import logging
from urllib import response
from config import BOT_TOKEN, API_TOKEN  # Importar los tokens del bot y de la API desde un archivo de configuración.
from weather_request import *  # Funciones relacionadas con la obtención del clima.
from counter import *  # Funciones para manejar contadores.
from openai_code import *  # Funciones para interactuar con OpenAI.

from telegram import Update, ReplyKeyboardMarkup, ParseMode  # Módulos de Telegram necesarios para manejar mensajes y teclados.
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters  # Módulos para manejar comandos y mensajes.

# Configuración del logger para registrar eventos e información de depuración.
logger = logging.getLogger(__name__)

# Texto del menú y botones
MENU = "¿Qué necesitas?"  # Mensaje principal del menú.
CLIMA_BUTTON = "🌤️ Quiero saber el clima!"  # Botón para consultar el clima.
CONTAR_BUTTON = "🔢 Quiero contar!"  # Botón para incrementar un contador.
IA_BUTTON = "🤖 Analizar chat"  # Botón para analizar una conversación.

# Crear un teclado personalizado con las opciones disponibles.
MENU_KEYBOARD = ReplyKeyboardMarkup(
    [[CLIMA_BUTTON], [CONTAR_BUTTON], [IA_BUTTON]],  # Disposición de los botones.
    resize_keyboard=True,  # Ajustar el tamaño del teclado al contenido.
    one_time_keyboard=True  # Hacer que el teclado desaparezca después de usarlo.
)

# Función para manejar el contador.
def count(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)  # Obtener el ID del usuario.
    counters = load_counters()  # Cargar los contadores existentes.

    # Si el usuario no tiene un contador, se inicializa en 0.
    if user_id not in counters:
        counters[user_id] = 0

    counters[user_id] += 1  # Incrementar el contador del usuario.

    save_counters(counters)  # Guardar los contadores actualizados.

    response = f"Tu contador actual es: {counters[user_id]}"
    context.user_data["last_bot_response"] = response  # Guarda la última respuesta del bot

    context.bot.send_message(chat_id=update.effective_user.id, text=response)# Enviar un mensaje al usuario con su contador actualizado.
    almacenar_chat(update, context)  # Almacena el historial del chat

# Función para obtener y mostrar el clima.
def weather(update: Update, context: CallbackContext) -> None:
    datos_clima = get_weather_info("Montevideo", API_TOKEN)  # Obtener datos del clima usando la API.

    # Extraer la información relevante del clima.
    clima = datos_clima['weather'][0]['description']
    temperatura = datos_clima['main']['temp']
    humedad = datos_clima['main']['humidity']
    viento = datos_clima['wind']['speed']

    # Generar recomendaciones basadas en las condiciones climáticas.
    if "lluvia" in clima.lower():
        recomendacion = "Lleva un paraguas, parece que va a llover."
    elif float(temperatura) > 25:
        recomendacion = "Hace mucho calor, no olvides hidratarte."
    elif float(temperatura) < 10:
        recomendacion = "Hace frío, lleva un abrigo."
    else:
        recomendacion = "El clima parece agradable, ¡disfruta tu día!"

    # Crear el mensaje completo con la información del clima.
    weather_message = (
        f"Clima en Montevideo:\n"
        f"- Condiciones: {clima}\n"
        f"- Temperatura: {temperatura}°C\n"
        f"- Humedad: {humedad}%\n"
        f"- Viento: {viento} m/s\n"
        f"{recomendacion}"
    )

    extra_message = generar_respuesta_inteligente("Montevideo") #Agrego comentario de clima generado por IA
    weather_message += f"\n\n{extra_message}"
    
    context.user_data["last_bot_response"] = weather_message  # Guarda la respuesta del bot
    update.message.reply_text(weather_message)# Enviar el mensaje al usuario.
    almacenar_chat(update, context)  # Almacena el historial del chat



# Función para analizar conversaciones usando IA
def analizar_conversacion(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_user.id
    chat_history = context.user_data.get("chat_history", "")  # Obtiene el historial de conversación

    if not chat_history:
        # Si no hay historial suficiente, informa al usuario
        context.bot.send_message(
            chat_id=chat_id,
            text="No hay suficiente historial de conversación para analizar."
        )
        return

    # Analiza el sentimiento de la conversación
    resultado = analizar_sentimiento(chat_history)
    response=f"Análisis de Sentimiento:\n\n{resultado}"

    context.user_data["last_bot_response"] = response  # Guarda la última respuesta del bot
    context.bot.send_message(
        chat_id=chat_id,
        text=response
    )
    almacenar_chat(update, context)  # Almacena el historial del chat


def almacenar_chat(update: Update, context: CallbackContext) -> None:
    """
    Almacena el historial de conversación entre el usuario y el bot.
    """
    user_message = update.message.text
    bot_response = context.user_data.get("last_bot_response", "")

    # Almacena el historial en user_data
    chat_history = context.user_data.get("chat_history", [])
    if bot_response:
        chat_history.append(f"Bot: {bot_response}")
    chat_history.append(f"Usuario: {user_message}")
    context.user_data["chat_history"] = chat_history

    # Procesa el texto (llama a funciones si es necesario)
    #handle_text(update, context)


# Función para mostrar el menú principal
def menu(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=MENU_KEYBOARD  # Muestra el teclado personalizado
    )

# Maneja las opciones del teclado personalizado
def handle_text(update: Update, context: CallbackContext) -> None:
    text = update.message.text  # Obtiene el texto enviado por el usuario

    # Ejecuta la función correspondiente según el botón seleccionado
    if text == CLIMA_BUTTON:
        response = "Aquí tienes información del clima:"
        weather(update, context)
    elif text == CONTAR_BUTTON:
        response = "Contando..."
        count(update, context)
    elif text == IA_BUTTON:
        response = "Analizando conversación..."
        analizar_conversacion(update, context)
    else:
        response = MENU
        context.user_data["last_bot_response"] = response
        menu(update, context)  # Si no coincide, muestra el menú nuevamente

    context.user_data["last_bot_response"] = response

# Función que se ejecuta al iniciar el bot
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="¡Hola! Estoy aquí para ayudarte. 😄"
    )
    menu(update, context)

# Configuración principal del bot
def main() -> None:
    updater = Updater(BOT_TOKEN)  # Inicializa el bot con el token

    dispatcher = updater.dispatcher  # Obtiene el dispatcher para registrar handlers

    # Registra los comandos y manejadores
    dispatcher.add_handler(CommandHandler("start", start))  # Comando /start
    dispatcher.add_handler(CommandHandler("menu", menu))    # Comando /menu
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))  # Manejo de texto
    # Inicia el bot
    updater.start_polling()

    # Mantiene el bot corriendo hasta que se detenga manualmente
    updater.idle()

# Punto de entrada del programa
if __name__ == '__main__':
    main()