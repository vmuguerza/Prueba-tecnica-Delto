import json
from config import COUNTER_FILE

# Cargar los contadores desde el archivo
def load_counters():
    try:
        with open(COUNTER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Guardar los contadores en el archivo
def save_counters(counters):
    with open(COUNTER_FILE, "w") as file:
        json.dump(counters, file)