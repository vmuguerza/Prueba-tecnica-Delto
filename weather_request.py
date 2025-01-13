
import requests

def get_weather_info(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Verifica si hubo un error en la solicitud
        
        
        datos = respuesta.json()
        

        return datos
    
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos del clima: {e}")


