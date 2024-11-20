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

# Define la lista de edificios (si prefieres mantenerla aquí)
edificios = [
    (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4), (5, 2), (5, 3), (5, 4),
    (2, 7), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8), (5, 8), (2, 9), (3, 9), (4, 9), (5, 9), 
    (2, 10), (3, 10), (4, 10), (5, 10), (2, 11), (3, 11), (5, 11),
    (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 10), (8, 11), (9, 3), (9, 4), 
    (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (10, 2), (10, 3), (10, 4), (10, 5), 
    (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (11, 2), (11, 3), (11, 4), (11, 5), (11, 7), 
    (11, 8), (11, 9), (11, 10), (11, 11), (16, 2), (16, 3), (16, 4), (16, 5), (17, 3), (17, 4), 
    (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (21, 5), (16, 8), (16, 9), 
    (16, 10), (16, 11), (17, 8), (17, 9), (17, 10), (17, 11), (18, 8), (18, 9), (18, 10), (19, 8), 
    (19, 9), (19, 10), (19, 11), (20, 9), (20, 10), (20, 11), (21, 8), (21, 9), (21, 10), (21, 11), 
    (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (11, 16), (2, 17), 
    (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (2, 20), (3, 20), 
    (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (11, 20), (10, 20), (2, 21), (3, 21), (4, 21), 
    (5, 21), (6, 21), (7, 21), (9, 21), (10, 21), (11, 21), (16, 16), (16, 17), (17, 16), 
    (16, 20), (16, 21), (17, 20), (17, 21), (20, 16), (20, 17), (21, 16), (21, 17), (20, 20), 
    (20, 21), (21, 21), (13, 13), (14, 13), (14, 14), (13, 14),
]

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
    city_model.step()
    plot_grid(city_model, ax)
    plt.draw()
    plt.pause(0.1)

plt.ioff()
plt.show()


