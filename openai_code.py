import openai

def analizar_sentimiento(conversacion):
    """
    Envía la conversación del usuario a OpenAI para analizar el sentimiento.
    """
    try:
        respuesta = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=(
                f"""Analiza el siguiente texto y clasifica el sentimiento como positivo,
                negativo o neutral. También proporciona una breve explicación:\n\n
                {conversacion}\n\n
                Clasificación:"""
            ),
            max_tokens=50,
            temperature=0.7,
        )
        texto = respuesta.choices[0].text.strip()
        return texto
    except Exception as e:
        return f"Error al analizar el sentimiento: {e}"

def generar_respuesta_inteligente(ciudad):
    """
    Usa OpenAI para generar una respuesta adicional sobre el clima o la ciudad.
    """
    try:
        respuesta = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=(
                f"""Proporciona un consejo útil o un dato interesante sobre el clima en {ciudad} 
                para mejorar la experiencia del usuario:"""
            ),
            max_tokens=100,
            temperature=0.7,
        )
        texto = respuesta.choices[0].text.strip()
        return texto
    except Exception as e:
        return f"Error al generar respuesta adicional: {e}"

