from model_city import cityClass
import matplotlib.pyplot as plt
from traffic_light import Traffic_light
from car_agent import CarAgent

def show_grid(model):
    grid = model.grid
    visual = [[0 for _ in range(model.width)] for _ in range(model.height)]
    for (cell_contents, x, y) in model.grid.coord_iter():
        for agent in cell_contents:
            if isinstance(agent, Traffic_light):
                visual[y][x] = 2  # Semáforo
            elif isinstance(agent, CarAgent):
                visual[y][x] = 1  # Carro
    plt.imshow(visual, cmap='viridis', interpolation='nearest')
    plt.xticks(range(model.width))
    plt.yticks(range(model.height))
    plt.grid(which='both', color='black', linewidth=1)
    plt.show()

# Crear un modelo
city = cityClass()

# Plotear el modelo inicial
show_grid(city)

# Ejecutar el modelo y visualizar cada paso
for i in range(10):
    print(f"Paso {i+1}")
    city.step()
    show_grid(city)
