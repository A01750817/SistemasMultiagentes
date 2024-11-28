# Actividad Integradora
# Codigo que muestra el tablero de la ciudad con los agentes y semaforos
# Autores:
# Santiago Villazón Ponce de León   A01746396
# Juan Antonio Figueroa Rodríguez   A01369043
# Iván Alexander Ramos Ramírez      A01750817
# Sebastián Antonio Almanza         A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from actividad_model import cityClass, CarAgent, Traffic_light, BuildingAgent, PersonAgent

# Define la lista de edificios
edificios = [
    #Edificio 1:
        (3, 3), (4, 3), (5, 3), (6, 3),
        (3, 4), (4, 4), (5, 4), (6, 4), 
        (3, 5), (4, 5), (6, 5), (6, 5),

        #Edificio 2:
        (3, 10), (4, 10), (5, 10), (6, 10),
        (3, 11), (4, 11), (5, 11), (6, 11),
        (3, 12), (4, 12), (5, 12), (6, 12),
        (3, 13), (4, 13), (5, 13), (6, 13),
        (3, 14), (4, 14), (5, 14), (6, 14),

        #Edificio 3:
        (11, 3), (12, 3), (13, 3), (14, 3),
        (11, 4), (12, 4), (13, 4), (14, 4),
        (11, 5), (12, 5), (13, 5), (14, 5),
        (11, 6), (12, 6), (13, 6), (14, 6),
        (11, 7), (12, 7), (13, 7), (14, 7),
        (11, 8), (12, 8), (13, 8), (14, 8),
        (11, 9), (12, 9), (13, 9), (14, 9),
        (11, 10), (12, 10), (13, 10), (14, 10),
        (11, 11), (12, 11), (13, 11), (14, 11),
        (11, 12), (12, 12), (13, 12), (14, 12),
        (11, 13), (12, 13), (13, 13), (14, 13),
        (11, 14), (12, 14), (13, 14), (14, 14),
        
        #Edificio 4:
        (19, 3), (20, 3),
        (19, 4), (20, 4),
        (19, 5), (20, 5),
        (19, 6), (20, 6), 

        #Edificio 5:
        (25, 3), (26, 3), 
        (25, 4), (26, 4),
        (25, 5), (26, 5),
        (25, 6), (26, 6),

        #Edificio 6:
        (19, 11), (20, 11), (21, 11), (22, 11), (23, 11), (24, 11), (25, 11), (26, 11),
        (19, 12), (20, 12), (21, 12), (22, 12), (23, 12), (24, 12), (25, 12), (26, 12),
        (19, 13), (20, 13), (21, 13), (22, 13), (23, 13), (24, 13), (25, 13), (26, 13),
        (19, 14), (20, 14), (21, 14), (22, 14), (23, 14), (24, 14), (25, 14), (26, 14), 

        #Rotonda
        (16, 17), (17, 17),
        (16, 18), (17, 18),
        
        #Edificio 8:
        (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21), (10, 21), (11, 21),(12, 21), (13, 21), (14, 21),
        (3, 22), (4, 22), (5, 22), (6, 22), (7, 22), (8, 22), (9, 22), (10, 22), (11, 22), (12, 22), (13, 22), (14, 22),

        #Edificio 9:
        (3, 27), (4, 27), (5, 27), (6, 27), (7, 27), (8, 27), (9, 27), (10, 27), (11, 27), (12, 27), (13, 27), (14, 27),
        (3, 28), (4, 28), (5, 28),(6, 28), (7, 28), (8, 28), (9, 28), (10, 28), (11, 28), (12, 28), (13, 28), (14, 28),
        
        #Edificio 10:
        (19, 21), (20, 21),
        (19, 22), (20, 22),

        #Edificio 11:
        (25, 21), (26, 21),
        (25, 22), (26, 22),

        #Edificio 12:
        (19, 27), (20, 27),
        (19, 28), (20, 28),

        #Edificio 13:
        (25, 27), (26, 27),
        (25, 28), (26, 28),
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
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='lightblue')
        ax.add_patch(rect)

    # Dibujar Banquetas
    for (x, y) in model.side_walk:
        color = 'gray'  # Color por defecto
        cell_contents = model.grid.get_cell_list_contents((x, y))
        for agent in cell_contents:
            if hasattr(agent, "color"):
                color = agent.color  # Color dinámico si está definido
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)

    # Dibujar garajes
    for (x, y) in model.garajes:
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='yellow')
        ax.add_patch(rect)

    # Dibujar direcciones permitidas
    colores_direcciones = {
        'left': 'white', #'red',
        'right': 'white', #'green',
        'down': 'white', #'cyan',
        'up': 'white', #'magenta',
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

    colores_direcciones_peat = {
        'left': 'red',
        'right': 'blue',
        'down': 'cyan',
        'up': 'magenta',
    }

    # Dibujar direcciones permitidas para peatones (todas en azul)
    for pos, directions_p in model.direcciones_peatones.items():
        for direction_p in directions_p:
            if direction_p == 'left':
                dx, dy = -0.45, 0.5
                ax.annotate("<-", (pos[0] + dx, pos[1] + dy), color=colores_direcciones_peat[direction_p], fontsize=8, ha='center')
            elif direction_p == 'right':
                dx, dy = 0.45, 0.5
                ax.annotate("->", (pos[0] + 1 + dx, pos[1] + dy), color=colores_direcciones_peat[direction_p], fontsize=8, ha='center')
            elif direction_p == 'up':
                dx, dy = 0.5, -0.45
                ax.annotate("^", (pos[0] + dx, pos[1] + dy), color=colores_direcciones_peat[direction_p], fontsize=8, ha='center')
            elif direction_p == 'down':
                dx, dy = 0.5, 0.45
                ax.annotate("v", (pos[0] + dx, pos[1] + 1 + dy), color=colores_direcciones_peat[direction_p], fontsize=8, ha='center')


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
            elif isinstance(obj, PersonAgent):
                circle = patches.Circle((x + 0.5, y + 0.5), 0.4, linewidth=1, edgecolor='black', facecolor='blue')
                ax.add_patch(circle)
            elif isinstance(obj, BuildingAgent):
                rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='gray')
                ax.add_patch(rect)
            



# Configuración inicial de la simulación
num_agents_car = 17  # Número de carros
num_agents_person = 10  # Número de peatones
city_model = cityClass(numberAgents=num_agents_car, numberAgentsP=num_agents_person, width=32, height=32)

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



