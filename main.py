
import logging
from config import BOT_TOKEN,API_TOKEN
from weather_request import *
from counter import *
from openai_code import *

from telegram import Update,  InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)

# Pre-assign menu text
MENU = "<b>Menu</b>\n\n Hola que nesecitas?"


# Pre-assign button text
CLIMA_BUTTON = "Quiero saber el clima!"
CONTAR_BUTTON = "Quiero contar!"
IA_BUTTON = "Analizar chat"


# Build keyboards
MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(CLIMA_BUTTON, callback_data=CLIMA_BUTTON)],
    [InlineKeyboardButton(CONTAR_BUTTON, callback_data=CONTAR_BUTTON)],
    [InlineKeyboardButton(IA_BUTTON, callback_data=IA_BUTTON)]
    ])


# Función para manejar el contador
def count(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)
    counters = load_counters()

    # Incrementar el contador del usuario
    if user_id not in counters:
        counters[user_id] = 0

    counters[user_id] += 1

    # Guardar los contadores actualizados
    save_counters(counters)

    # Enviar mensaje al usuario con el valor actualizado
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"Tu contador actual es: {counters[user_id]}"
    )

def weather(update: Update, context: CallbackContext) -> None:

    datos_clima=get_weather_info("Montevideo", API_TOKEN)

    clima = datos_clima['weather'][0]['description']
    temperatura = datos_clima['main']['temp']
    humedad = datos_clima['main']['humidity']
    viento = datos_clima['wind']['speed']

    # Recomendaciones basadas en el clima
    if "lluvia" in clima.lower():
        recomendacion = "Lleva un paraguas, parece que va a llover."
    elif float(temperatura) > 25:
        recomendacion = "Hace mucho calor, no olvides hidratarte."
    elif float(temperatura) < 10:
        recomendacion = "Hace frío, lleva un abrigo."
    else:
        recomendacion = "El clima parece agradable, ¡disfruta tu día!"


    weather_message=(
        f"Clima en Montevideo:\n"
        f"- Condiciones: {clima}\n"
        f"- Temperatura: {temperatura}°C\n"
        f"- Humedad: {humedad}%\n"
        f"- Viento: {viento} m/s\n"
        f"{recomendacion}"
    )

    extra_message = generar_respuesta_inteligente("Montevideo")
    weather_message += f"\n\n{extra_message}"
    
    update.callback_query.message.reply_text(weather_message)

def analizar_conversacion(update: Update, context: CallbackContext) -> None:
    """
    Analiza la conversación entre el usuario y el bot.
    """
    chat_id = update.effective_user.id
    chat_history = context.user_data.get("chat_history", "")

    if not chat_history:
        context.bot.send_message(
            chat_id=chat_id,
            text="No hay suficiente historial de conversación para analizar."
        )
        return

    resultado = analizar_sentimiento(chat_history)
    context.bot.send_message(
        chat_id=chat_id,
        text=f"Análisis de Sentimiento:\n\n{resultado}"
    )



def menu(update: Update, context: CallbackContext) -> None:

    context.bot.send_message(
        update.message.from_user.id,
        MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=MENU_MARKUP
    )


def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    data = update.callback_query.data

    if data == CLIMA_BUTTON:
        weather(update, context)
    elif data == CONTAR_BUTTON:
        count(update, context)
    elif data== IA_BUTTON:
        analizar_conversacion(update,context)

    # Close the query to end the client-side loading animation
    update.callback_query.answer()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("¡Hola! Estoy aquí para ayudarte.")
    menu(update, context) 

def main() -> None:
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))

    # Register handler for inline buttons
    dispatcher.add_handler(CallbackQueryHandler(button_tap))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()



if __name__ == '__main__':
    main()
