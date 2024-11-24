from flask import Flask, request, jsonify
import threading
from actividad_model import cityClass, CarAgent  # Importa tu modelo y la clase CarAgent

app = Flask(__name__)

# Crear una instancia global del modelo de Mesa
number_of_agents = 10  # Ajusta según sea necesario
city_model = cityClass(numberAgents=number_of_agents, width=24, height=24)

# Lock para sincronizar el acceso al modelo
model_lock = threading.Lock()

# Función para ejecutar el modelo en un hilo separado
def run_model():
    while True:
        with model_lock:
            city_model.step()

# Iniciar el hilo del modelo
model_thread = threading.Thread(target=run_model)
model_thread.daemon = True
model_thread.start()

# Ruta para enviar coordenadas a Unity
@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    with model_lock:
        coordinates = []

        # Iterar sobre todos los agentes en el modelo
        for agent in city_model.schedule.agents:
            if isinstance(agent, CarAgent):  # Filtrar solo los agentes de tipo CarAgent
                coord = {
                    'id': agent.unique_id,
                    'x': agent.pos[0],
                    'y': agent.pos[1],
                    'z': 0  # Ajusta si trabajas en un entorno 3D
                }
                coordinates.append(coord)

    return jsonify({'agents': coordinates})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
