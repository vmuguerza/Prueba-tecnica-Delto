# Chat Bot de Telegram - Prueba Técnica para Delto

Este proyecto es un chatbot desarrollado para Telegram que proporciona información sobre el clima y funcionalidades adicionales, como un contador persistente de interacciones. También está integrado con la API de OpenAI para analizar conversaciones y generar comentarios relacionados con el clima.

## Funcionalidades

1. **Información del clima:**
   - El chatbot responde con la informacion climatica actual en la ciudad de Montevideo.
   - Utiliza una API meteorológica (OpenWeather) para obtener datos actualizados.

2. **Integración con OpenAI:**
   - Analiza el historial de conversaciones para determinar el sentimiento (positivo, negativo, neutral).
   - Genera comentarios útiles o interesantes relacionados con el clima.
   - **Nota:** Actualmente, la funcionalidad de OpenAI no está habilitada debido a la falta de créditos de prueba para obtener un token de API.

3. **Contador persistente:**
   - Registra y almacena de manera persistente el número de interacciones de los usuarios con el chatbot.

## Tecnologías Utilizadas

- **Python:** Lenguaje principal para el desarrollo del bot.
- **Telegram Bot API:** Para la interacción con los usuarios en Telegram.
- **OpenAI API:** (Integración no funcional actualmente).
- **Base de datos:** Para la persistencia del contador (archivo JSON).
- **API Meteorológica:** Para obtener datos del clima (OpenWeatherMap).

## Requisitos Previos

- **Token de Telegram:** Necesario para configurar el bot en la plataforma.
- **API Key de la API Meteorológica:** Requerida para consultar información climática.
- **Token de OpenAI:** Requerida para la funcionalidad de análisis de sentimientos y generación de comentarios.

## Instalación y Configuración

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
3. Configura las variables de entorno:
   - Crea un archivo .env en la raiz del proyecto
   - Agrega las sigueintes claves:
     ```markfile
     TELEGRAM_TOKEN=<tu_token_de_telegram>
      WEATHER_API_KEY=<tu_api_key_del_clima>
      OPENAI_API_KEY=<tu_token_de_openai>
4. Ejecuta el bot
      ```bash
      python main.py

   
