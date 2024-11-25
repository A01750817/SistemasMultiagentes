from flask import Flask, jsonify
from actividad_model import cityClass
from car_agent import CarAgent

app = Flask(__name__)

# Instancia del modelo
num_agents = 10  # Cambia según el número de agentes
city_model = cityClass(numberAgents=num_agents)

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    """Devuelve las coordenadas de los agentes al cliente (Unity)."""
    agent_positions = [
        {
            "id": agent.unique_id,
            "x": agent.pos[0] * 10,  # Factor de escala para Unity
            "y": 0,  # Altura constante
            "z": agent.pos[1] * 10  # Factor de escala para Unity
        }
        for agent in city_model.schedule.agents if isinstance(agent, CarAgent)
    ]
    return jsonify(agent_positions)

@app.route('/step_simulation', methods=['POST'])
def step_simulation():
    """Avanza un paso en la simulación."""
    city_model.step()
    return jsonify({"message": "Simulation stepped successfully."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
