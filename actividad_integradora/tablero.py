import matplotlib.pyplot as plt
import matplotlib.patches as patches
from actividad_model import cityClass, CarAgent, Traffic_light

edificios = [(2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]

def plot_grid(model):
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_xlim(0, model.grid.width)
    ax.set_ylim(0, model.grid.height)
    ax.xaxis.tick_top()
    ax.set_xticks(range(1, model.grid.width + 1))
    ax.set_xticklabels(range(1, model.grid.width + 1), ha='center')
    ax.invert_yaxis()
    ax.set_yticks(range(1, model.grid.height + 1))
    ax.set_yticklabels(range(1, model.grid.height + 1), va='center')
    ax.grid(which="both")

    for (x, y) in edificios:
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='blue')
        ax.add_patch(rect)

    for cell, (x, y) in model.grid.coord_iter():
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

# Inicializar y simular el modelo
city_model = cityClass()
for _ in range(1000):  # Ejecutar 10 pasos de simulación
    city_model.step()
    plot_grid(city_model)


