import matplotlib.pyplot as plt
import matplotlib.patches as patches
from actividad_model import cityClass

def plot_grid(model):
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_xlim(0, model.grid.width)
    ax.set_ylim(0, model.grid.height)
    ax.set_xticks(range(model.grid.width))
    ax.set_yticks(range(model.grid.height))
    ax.grid(which="both")
    
    for (x, y) in model.grid.coord_iter():
        cell_content = model.grid.get_cell_list_contents((x, y))
        for obj in cell_content:
            if isinstance(obj, CarAgent):
                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='blue')
                ax.add_patch(rect)
            elif isinstance(obj, Traffic_light):
                color = 'green' if obj.state else 'red'
                circle = patches.Circle((x + 0.5, y + 0.5), 0.4, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(circle)

    plt.show()

# Crear una instancia del modelo y ejecutar algunos pasos
city_model = cityClass()
for _ in range(10):  # Ejecuta 10 pasos de simulación
    city_model.step()
    plot_grid(city_model)