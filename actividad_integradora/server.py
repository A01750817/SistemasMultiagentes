from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta para enviar coordenadas a Unity
@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    coordinates = {'x': 10.0, 'y': 20.0, 'z': 30.0}  # Ejemplo de coordenadas
    return jsonify(coordinates)

# Ruta para recibir coordenadas de Unity
@app.route('/send_coordinates', methods=['POST'])
def send_coordinates():
    data = request.json
    print(f"Received coordinates from Unity: {data}")
    return jsonify({'message': 'Coordinates received successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Asegúrate de usar el mismo puerto en Unity