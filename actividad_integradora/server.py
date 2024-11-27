from flask import Flask, jsonify
from actividad_model import cityClass
from car_agent import CarAgent
from person_agent import PersonAgent

app = Flask(__name__)

# Instancia del modelo
num_agentsA = 17 
num_agentsP = 20 # Cambia según el número de agentes
city_model = cityClass(numberAgents=num_agentsA, numberAgentsP=num_agentsP, width=32, height=32)

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    """Devuelve las coordenadas de los agentes al cliente (Unity)."""
    scale = 1.4  # Ajusta según el cálculo de escala
    offset_x = -12  # Offset para centrar el mapa en Unity
    offset_z = 20  # Offset para centrar el mapa en Unity
    road_height = 0.001  # Altura fija para los coches en Unity
    sidewalk_height = 0.19  # Altura fija para los peatones en Unity

    # Transformación de coordenadas de los agentes coche
    car_positions = [
        {
            "id": agent.unique_id,
            "x": agent.pos[0] * scale,
            "y": road_height,
            "z": -agent.pos[1] * scale
        }
        for agent in city_model.schedule.agents if isinstance(agent, CarAgent)
    ]

    # Transformación de coordenadas de los agentes peatones
    pedestrian_positions = [
        {
            "id": agent.unique_id,
            "x": agent.pos[0] * scale,
            "y": sidewalk_height,
            "z": -agent.pos[1] * scale
        }
        for agent in city_model.schedule.agents if isinstance(agent, PersonAgent)
    ]

    # Combina ambas listas en un único JSON
    agent_positions = {
        "car_positions": car_positions,
        "pedestrian_positions": pedestrian_positions
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
