# tablero.py
# Actividad Integradora
# Codigo que muestra el tablero de la ciudad con los agentes y semaforos
# Autores:
# Santiago Villazón Ponce de León	A01746396
# Juan Antonio Figueroa Rodríguez	A01369043
# Iván Alexander Ramos Ramírez		A01750817
# Sebastián Antonio Almanza			A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from actividad_model import cityClass, CarAgent, Traffic_light, BuildingAgent

def plot_grid(model, ax):
    ax.clear()
    ax.set_xlim(0, model.width)
    ax.set_ylim(0, model.height)
    ax.xaxis.tick_top()
    ax.set_xticks(range(model.width))
    ax.set_xticklabels(range(1, model.width + 1), ha='center')
    ax.invert_yaxis()
    ax.set_yticks(range(model.height))
    ax.set_yticklabels(range(1, model.height + 1), va='center')
    ax.grid(which="both")

    # Dibujar edificios
    for (x, y) in model.celdas_restringidas:
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='blue')
        ax.add_patch(rect)

    # Dibujar garajes
    for (x, y) in model.garajes:
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='yellow')
        ax.add_patch(rect)

    # Dibujar direcciones permitidas (opcional, si deseas incluir flechas)
    colores_direcciones = {
        'left': 'red',
        'right': 'green',
        'down': 'cyan',
        'up': 'magenta',
    }
    for pos, directions in model.direcciones_permitidas.items():
        for direction in directions:
            if direction == 'left':
                dx, dy = -0.45, 0.5
                ax.annotate("<-", (pos[0] + dx, pos[1] + dy), color=colores_direcciones[direction], fontsize=8, ha='center')
            elif direction == 'right':
                dx, dy = 0.45, 0.5
                ax.annotate("->", (pos[0] + 1 + dx, pos[1] + dy), color=colores_direcciones[direction], fontsize=8, ha='center')
            elif direction == 'up':
                dx, dy = 0.5, -0.45
                ax.annotate("^", (pos[0] + dx, pos[1] + dy), color=colores_direcciones[direction], fontsize=8, ha='center')
            elif direction == 'down':
                dx, dy = 0.5, 0.45
                ax.annotate("v", (pos[0] + dx, pos[1] + 1 + dy), color=colores_direcciones[direction], fontsize=8, ha='center')

    # Dibujar agentes y semáforos
    for (contents, (x, y)) in model.grid.coord_iter():
        for obj in contents:
            if isinstance(obj, CarAgent):
                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='orange')
                ax.add_patch(rect)
            elif isinstance(obj, Traffic_light):
                color = 'green' if obj.state else 'red'
                circle = patches.Circle((x + 0.5, y + 0.5), 0.4, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(circle)
            elif isinstance(obj, BuildingAgent):
                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='gray')
                ax.add_patch(rect)

# Configuración inicial de la simulación
num_agents = 17  # Cambia este número para ajustar la cantidad de agentes
city_model = cityClass(numberAgents=num_agents, width=24, height=24)

# Número de pasos de la simulación
n_steps = 300
plt.ion()
fig, ax = plt.subplots(figsize=(8, 8))

# Ciclo de simulación
for step in range(n_steps):
    print(f"\n### Step {step} ###")
    city_model.step()
    plot_grid(city_model, ax)
    plt.draw()
    plt.pause(0.1)

plt.ioff()
plt.show()
