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
from actividad_model import cityClass, CarAgent, Traffic_light

# Define buildings and garage positions
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
garajes = [(4,4), (4, 11), (2, 8), (8, 9), (9, 2), (10, 11), (11, 6), (17, 2), (20, 5), (20, 8), 
           (18, 11), (3, 17), (10, 16), (4, 20), (8, 21), (17, 17), (21, 20)]



# Direcciones (ya definidas en actividad_model.py)
direcciones_izquierda = [
    [(x, y) for x in range(25) for y in range(0,2)],
    [(x, y) for x in range(2,8) for y in range(5,7)],
    [(x, y) for x in range(2,14) for y in range(12,14)],
    [(x, y) for x in range(16,24) for y in range(12,14)],
    [(x, y) for x in range(16,24) for y in range(18,20)],
    [(x, y) for x in range(13, 17) for y in range(12, 13)],
    [(2, 8), (8, 9), (12, 6), (17, 2), (20, 5), (18, 17), (22, 20)]
]

direcciones_derecha = [
    [(x, y) for x in range(0,12) for y in range(14,16)],
    [(x, y) for x in range(0,12) for y in range(18,20)],
    [(x, y) for x in range(14,22) for y in range(14,16)],
    [(x, y) for x in range(14,22) for y in range(6,8)],
    [(x, y) for x in range(-1, 24) for y in range(22,24)],
    [(x, y) for x in range(11, 15) for y in range(15, 16)],
    [(1, 8), (7, 9), (11, 6), (18, 2), (19, 5), (17, 17), (21, 20)]
]

direcciones_abajo = [
    [(x, y) for x in range(2) for y in range(-1, 24)],
    [(x, y) for x in range(6, 8) for y in range(0, 12)],
    [(x, y) for x in range(12, 14) for y in range(0, 12)],
    [(x, y) for x in range(12, 14) for y in range(14, 22)],
    [(x, y) for x in range(18, 20) for y in range(14, 22)],
    [(x, y) for x in range(12, 13) for y in range(12, 15)],
    [(9, 1), (4, 19), (8, 21), (3, 17), (4, 4), (4, 11), (10, 11), 
     (18, 11), (20, 7), (10, 15), (17, 1), (20, 5), (17, 17), (21, 19)]
]

direcciones_arriba = [
    [(x, y) for x in range(22, 24) for y in range(0, 25)],
    [(x, y) for x in range(14, 16) for y in range(2, 14)],
    [(x, y) for x in range(14, 16) for y in range(16, 24)],
    [(x, y) for x in range(18, 20) for y in range(2, 8)],
    [(x, y) for x in range(15, 16) for y in range(12, 17)],
    [(9, 2), (4, 20), (8, 22), (3, 18), (4, 5), (4, 12), (10, 12), 
     (18, 12), (20, 8), (10, 16), (17, 2), (20, 6), (17, 18), (21, 20)]
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
    for (x, y) in garajes:
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='yellow')
        ax.add_patch(rect)

    # Colores para direcciones
    colores_direcciones = {
        'left': 'red',
        'right': 'green',
        'down': 'cyan',
        'up': 'magenta',
    }

    # Dibujar direcciones permitidas
    for pos, directions in model.direcciones_permitidas.items():
        for direction in directions:
            if direction == 'left':
                dx, dy = -0.45, 0.5
                ax.annotate("<-", (pos[0]+dx, pos[1]+dy), color=colores_direcciones[direction], fontsize=8, ha='center')
            elif direction == 'right':
                dx, dy = 0.45, 0.5
                ax.annotate("->", (pos[0]+1+dx, pos[1]+dy), color=colores_direcciones[direction], fontsize=8, ha='center')
            elif direction == 'up':
                dx, dy = 0.5, -0.45
                ax.annotate("^", (pos[0]+dx, pos[1]+dy), color=colores_direcciones[direction], fontsize=8, ha='center')
            elif direction == 'down':
                dx, dy = 0.5, 0.45
                ax.annotate("v", (pos[0]+dx, pos[1]+1+dy), color=colores_direcciones[direction], fontsize=8, ha='center')

    # Dibujar semáforos y agentes
    for cell, (x, y) in model.grid.coord_iter():
        cell_content = model.grid.get_cell_list_contents((x, y))
        for obj in cell_content:
            if isinstance(obj, CarAgent):
                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='orange')
                ax.add_patch(rect)
            elif isinstance(obj, Traffic_light):
                color = 'green' if obj.state else 'red'
                circle = patches.Circle((x + 0.5, y + 0.5), 0.4, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(circle)

# Run the model and plot
num_agents = 5  
city_model = cityClass(numberAgents=1, width=24, height=24)


n_steps = 300 #Modificar en caso de querer probar mas pasos
plt.ion()
fig, ax = plt.subplots(figsize=(8, 8))

for step in range(n_steps):
    city_model.step()
    plot_grid(city_model, ax)
    plt.draw()
    plt.pause(0.1)

plt.ioff()
plt.show()
