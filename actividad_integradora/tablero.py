from model_city import cityClass  
import car_agent
import traffic_light
import matplotlib.pyplot as plt  

def show_grid(model):
    grid = model.grid
    # Mesa no tiene un método render() por defecto para SingleGrid, necesitarás definirlo
    grid_data = grid.grid  # Obtiene la cuadrícula
    # Crear una representación simple
    visual = [[0 for _ in range(model.width)] for _ in range(model.height)]
    for (x, y) in grid.coord_iter():
        cell = grid.get_cell_list_contents([(x, y)])
        for agent in cell:
            if isinstance(agent, traffic_light.Traffic_light):
                visual[y][x] = 2  # Semáforo
            elif isinstance(agent, car_agent.CarAgent):
                visual[y][x] = 1  # Carro
    plt.imshow(visual, cmap='viridis', interpolation='nearest')
    plt.show()

# Crear un modelo
city = cityClass()

# Ploatear el modelo inicial
show_grid(city)

# Ejecutar el modelo
for i in range(10):
    city.step()
    show_grid(city)