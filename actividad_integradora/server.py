from flask import Flask, jsonify
from actividad_model import cityClass
from car_agent import CarAgent

app = Flask(__name__)

# Instancia del modelo
num_agents = 17  # Cambia según el número de agentes
city_model = cityClass(numberAgents=num_agents)

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    """Devuelve las coordenadas de los agentes al cliente (Unity)."""
    scale = 2.4  # Ajusta según el cálculo de escala
    offset_x = -12  # Offset para centrar el mapa en Unity
    offset_z = 20  # Offset para centrar el mapa en Unity
    road_height = 0.001 # Altura fija para los agentes en Unity 0.001  

    # Transformación de coordenadas
    agent_positions = {
        "car_positions": [
            {
                "id": agent.unique_id,
                "x": agent.pos[0],
                "y": road_height,
                "z": -agent.pos[1]
            }
            for agent in city_model.schedule.agents if isinstance(agent, CarAgent)
        ]
    }
    return jsonify(agent_positions)




@app.route('/get_restrictions', methods=['GET'])
def get_restrictions():
    """Devuelve las restricciones y direcciones permitidas para las calles."""
    return jsonify({
        "restricted_cells": city_model.celdas_restringidas,
        "allowed_directions": city_model.direcciones_permitidas
    })

@app.route('/step_simulation', methods=['POST'])
def step_simulation():
    """Avanza un paso en la simulación."""
    city_model.step()
    return jsonify({"message": "Simulation stepped successfully."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
