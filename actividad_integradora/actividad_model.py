# Codigo que crea el modelo y genera los agentes y semaforos
# Autores:
# Santiago Villazón Ponce de León   A01746396
# Juan Antonio Figueroa Rodríguez   A01369043
# Iván Alexander Ramos Ramírez      A01750817
# Sebastián Antonio Almanza         A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024

import random
import mesa
from car_agent import CarAgent
from traffic_light import Traffic_light
from person_agent import PersonAgent

# Nueva clase BuildingAgent
class BuildingAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "building"  # Identificar el agente como edificio

class SideWalkAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super(). __init__(unique_id, model)
        self.type = "sidewalk"

#Clase que define el modelo de la ciudad y genera sus agentes
class cityClass(mesa.Model):
    """
    Clase que define el ambiente (ciudad) en el que los agentes carro navegan a un destino.
    ## Atributos:
    - num_agents (int): Número de agentes en la simulación.
    - width (int): Ancho de la cuadrícula de la ciudad.
    - height (int): Alto de la cuadrícula de la ciudad.
    - grid (mesa.space.MultiGrid): Cuadrícula que modela el espacio en el que los agentes interactúan.
    - schedule (mesa.time.RandomActivation): Scheduler del modelo.
    - running (bool): Estado de la simulación (True mientras está activa).
    - traffic_lights (list): Lista de semáforos presentes en la ciudad.
    - garajes (list): Coordenadas de garajes dentro de la cuadrícula.
    - celdas_restringidas (list): Coordenadas de las celdas restringidas.
    - direcciones_permitidas (dict): Diccionario que asocia coordenadas con direcciones válidas (izquierda, derecha, arriba, abajo).
    - initial_positions (list): Lista de posiciones iniciales de los agentes; si no se especifican, se asignan aleatoriamente.

    ## Métodos:
    - __init__(self, numberAgents=1, width=24, height=24): Inicializa la simulación con un número definido de agentes, tamaño de cuadrícula y otros parámetros.
    - _populate_allowed_directions(self, direction_lists, direction): Llena el diccionario `direcciones_permitidas` con las coordenadas válidas y sus respectivas direcciones.
    - create_traffic_lights(self): Crea y coloca semáforos en la cuadrícula en posiciones predefinidas que no estén restringidas.
    - create_agents(self): Crea agentes de tipo CarAgent y los asigna a posiciones iniciales con un destino en uno de los garajes.
    - step(self): Realiza un paso en la simulación, activando a los agentes en orden aleatorio.

    """
    def __init__(self, numberAgents=1, numberAgentsP=1, width=32, height=32):
        """
        Inicializa el modelo de celdas con los agentes, semaforos, altura y anchura del mapa y las celdas restringidas.
        ## Argumentos:
        - numberAgents (int): Número de agentes en la simulación.
        - width (int): Ancho de la cuadrícula de la ciudad.
        - height (int): Alto de la cuadrícula de la ciudad.
        """
        super().__init__()
        self.num_agents = numberAgents
        self.num_agents_p = numberAgentsP
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.traffic_lights = []
        self.side_walk = [
            #Celdas Banqueda Ed1:
            (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),
            (7, 3), (7, 4), (7, 5),
            (2, 3), (2, 4), (2, 5),
            (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),

            #Celdas Banqueda Ed2:
            (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9),
            (2, 10), (2, 11), (2, 12), (2, 13), (2, 14),
            (7, 10), (7, 11), (7, 12), (7, 13), (7, 14),
            (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), 

            #Celdas Banqueda Ed3:
            (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
            (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14),
            (15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14),
            (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15),

            #Celdas Banqueda Ed4:
            (20, 2), (21, 2), (22, 2), (23, 2),
            (20, 3), (20, 4), (20, 5), (20, 6),
            (23, 3), (23, 4), (23, 5), (23, 6),
            (20, 7), (21, 7), (22, 7), (23, 7),

            #Celdas Banqueda Ed5:
            (26, 2), (27, 2), (28, 2), (29, 2),
            (26, 3), (26, 4), (26, 5), (26, 6),
            (29, 3), (29, 4), (29, 5), (29, 6),
            (26, 7), (27, 7), (28, 7), (29, 7),

            #Celdas Banqueda Ed6:
            (20, 10), (21, 10), (22, 10), (23, 10), (24, 10), (25, 10), (26, 10), (27, 10), (28, 10), (29, 10),
            (20, 11), (20, 12), (20, 13), (20, 14),
            (29, 11), (29, 12), (29, 13), (29, 14),
            (20, 15), (21, 15), (22, 15), (23, 15), (24, 15), (25, 15), (26, 15), (27, 15), (28, 15), (29, 15),

            #Celdas Banqueda Ed8:
            (2, 20), (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20), (11, 20), (12, 20), (13, 20), (14, 20), (15, 20),
            (2, 21), (2, 22),
            (15, 21), (15, 22),
            (2, 23), (3, 23), (4, 23), (5, 23), (6, 23), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23), (13, 23), (14, 23), (15, 23),

            #Celdas Banqueda Ed9:
            (2, 26), (3, 26), (4, 26), (5, 26), (6, 26), (7, 26), (8, 26), (9, 26), (10, 26), (11, 26), (12, 26), (13, 26), (14, 26), (15, 26),
            (2, 27), (2, 28),
            (15, 27), (15, 28),
            (2, 29), (3, 29), (4, 29), (5, 29), (6, 29), (7, 29), (8, 29), (9, 29), (10, 29), (11, 29), (12, 29), (13, 29), (14, 29), (15, 29),

            #Celdas Banqueda Ed10:
            (20, 20), (21, 20), (22, 20), (23, 20),
            (20, 21), (20, 22),
            (23, 21), (23, 22),
            (20, 23), (21, 23), (22, 23), (23, 23),

             #Celdas Banqueda Ed11:
            (26, 20), (27, 20), (28, 20), (29, 20),
            (26, 21), (26, 22),
            (29, 21), (29, 22),
            (26, 23), (27, 23), (28, 23), (29, 23),

             #Celdas Banqueda Ed12:
            (20, 26), (21, 26), (22, 26), (23, 26),
            (20, 27), (20, 28),
            (23, 27), (23, 28),
            (20, 29), (21, 29), (22, 29), (23, 29),

             #Celdas Banqueda Ed13:
            (26, 26), (27, 26), (28, 26), (29, 26),
            (26, 27), (26, 28),
            (29, 27), (29, 28),
            (26, 29), (27, 29), (28, 29), (29, 29),
            


        ]

        self.garajes = [(5,5), 
                        (5, 14), (3, 11), 
                        (11, 10), (12, 3), (13, 14), (14, 7), 
                        (21, 3), 
                        (27, 6), 
                        (27, 11), (23, 14), 
                        (4, 22), (13, 21), 
                        (5, 27), (11, 28), 
                        (22, 22),
                        (28, 27)]
        
        self.celdas_restringidas = [
            #Celdas Banqueda Ed1:


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
            (21, 3), (22, 3),
            (21, 4), (22, 4),
            (21, 5), (22, 5),
            (21, 6), (22, 6), 

            #Edificio 5:
            (27, 3), (28, 3), 
            (27, 4), (28, 4),
            (27, 5), (28, 5),
            (27, 6), (28, 6),

            #Edificio 6:
            (21, 11), (22, 11), (23, 11), (24, 11), (25, 11), (26, 11), (27, 11), (28, 11),
            (21, 12), (22, 12), (23, 12), (24, 12), (25, 12), (26, 12), (27, 12), (28, 12),
            (21, 13), (22, 13), (23, 13), (24, 13), (25, 13), (26, 13), (27, 13), (28, 13),
            (21, 14), (22, 14), (23, 14), (24, 14), (25, 14), (26, 14), (27, 14), (28, 14), 

            #Rotonda
            (17, 17), (18, 17),
            (17, 18), (18, 18),
            
            #Edificio 8:
            (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21), (10, 21), (11, 21),(12, 21), (13, 21), (14, 21),
            (3, 22), (4, 22), (5, 22), (6, 22), (7, 22), (8, 22), (9, 22), (10, 22), (11, 22), (12, 22), (13, 22), (14, 22),

            #Edificio 9:
            (3, 27), (4, 27), (5, 27), (6, 27), (7, 27), (8, 27), (9, 27), (10, 27), (11, 27), (12, 27), (13, 27), (14, 27),
            (3, 28), (4, 28), (5, 28),(6, 28), (7, 28), (8, 28), (9, 28), (10, 28), (11, 28), (12, 28), (13, 28), (14, 28),
            
            #Edificio 10:
            (21, 21), (22, 21),
            (21, 22), (22, 22),

            #Edificio 11:
            (27, 21), (28, 21),
            (27, 22), (28, 22),

            #Edificio 12:
            (21, 27), (22, 27),
            (21, 28), (22, 28),

            #Edificio 13:
            (27, 27), (28, 27),
            (27, 28), (28, 28),
        ]

        # Define direcciones
        direcciones_izquierda = [
            [(x, y) for x in range(33) for y in range(0,2)],
            [(x, y) for x in range(2,10) for y in range(7,9)],
            [(x, y) for x in range(2,18) for y in range(16,18)],
            [(x, y) for x in range(20,32) for y in range(16,18)],
            [(x, y) for x in range(20,32) for y in range(24,26)],
            [(x, y) for x in range(15, 20) for y in range(16, 17)],
            #Salida ed 2 - grj1
            [(x, y) for x in range(2, 5) for y in range(11,12)],

            #Entrada ed 3 - grj2
            [(x, y) for x in range(15, 18) for y in range(7,8)],
            #Salida ed 3 - grj3
            [(x, y) for x in range(10, 13) for y in range(10, 11)],

            #Salida ed 4 - grj1
            [(x, y) for x in range(20, 23) for y in range(3,4)],

            #Salida ed 5 - grj1
            [(x, y) for x in range(26, 29) for y in range(6,7)],

            #Entrada ed 10 - grj1
            [(x, y) for x in range(23, 26) for y in range(22,23)],

            #Entrada ed 13 - grj1
            [(x, y) for x in range(29, 32) for y in range(27,28)],
        ]

        direcciones_derecha = [
            [(x, y) for x in range(0,16) for y in range(18, 20)],
            [(x, y) for x in range(0,16) for y in range(24, 26)],
            [(x, y) for x in range(18,30) for y in range(8, 10)],
            [(x, y) for x in range(18,30) for y in range(18, 20)],#
            [(x, y) for x in range(-1, 31) for y in range(30, 32)],
            [(x, y) for x in range(14, 19) for y in range(19, 20)],
            #Entrada ed 2 - grj1
            [(x, y) for x in range(0, 3) for y in range(11,12)],

            #Salida ed 3 - grj2
            [(x, y) for x in range(13, 16) for y in range(7,8)],
            #Entrada ed 3 - grj3
            [(x, y) for x in range(8, 11) for y in range(10, 11)],

            #Entrada ed 4 - grj1
            [(x, y) for x in range(18, 21) for y in range(3,4)],

            #Entrada ed 5 - grj1
            [(x, y) for x in range(24, 27) for y in range(6,7)],

            #Salida ed 10 - grj1
            [(x, y) for x in range(21, 24) for y in range(22,23)],

            #Salida ed 13 - grj1
            [(x, y) for x in range(27, 30) for y in range(27,28)],
        ]

        direcciones_abajo = [
            [(x, y) for x in range(2) for y in range(-1, 31)],
            [(x, y) for x in range(8, 10) for y in range(0, 16)],
            [(x, y) for x in range(16, 18) for y in range(0, 16)],
            [(x, y) for x in range(24, 26) for y in range(18, 30)],
            [(x, y) for x in range(16, 18) for y in range(18, 30)],
            [(x, y) for x in range(16, 17) for y in range(16, 19)],
            #Salidas ed 1 -  grj1
            [(x, y) for x in range(5, 6) for y in range(4,7)],

            #Salidas ed 2 - grj1
            [(x, y) for x in range(5, 6) for y in range(13,16)],

            #Entrada ed 3 - grj1
            [(x, y) for x in range(12, 13) for y in range(0,3)],
            #Salidas ed 3 - grj4
            [(x, y) for x in range(13, 14) for y in range(13,16)],

            #Entrada ed 4 - grj1
            [(x, y) for x in range(21, 22) for y in range(0,3)],

            #Salidas ed 5 - grj1
            [(x, y) for x in range(27, 28) for y in range(5,8)],


            #Entrada ed 6 - grj1
            [(x, y) for x in range(27, 28) for y in range(8,11)],
            #Salidas ed 6 - grj2
            [(x, y) for x in range(23, 24) for y in range(13,16)],

            #entrada ed 8 - grj1
            [(x, y) for x in range(13, 14) for y in range(18,21)],
            #Salidas ed 8 - grj2
            [(x, y) for x in range(4, 5) for y in range(21,24)],

            #Entrada ed 9 - grj1
            [(x, y) for x in range(5, 6) for y in range(24,27)],
            #Salidas ed 9 - grj2
            [(x, y) for x in range(11, 12) for y in range(27,30)],

            #Salidas ed 10 - grj1
            [(x, y) for x in range(22, 23) for y in range(21,24)],

            #Salida ed 13 - grj1
            [(x, y) for x in range(28, 29) for y in range(24,27)],
            
        ]

        direcciones_arriba = [
            [(x, y) for x in range(30, 32) for y in range(0, 33)],
            [(x, y) for x in range(18, 20) for y in range(2, 18)],
            [(x, y) for x in range(18, 20) for y in range(20, 32)],
            [(x, y) for x in range(24, 26) for y in range(2, 10)],
            [(x, y) for x in range(19, 20) for y in range(17, 20)],
            #Entrada grj1
            [(x, y) for x in range(5, 6) for y in range(6,9)],

            #Entrada ed 2 - grj1
            [(x, y) for x in range(5, 6) for y in range(15,18)],

            #Salida ed 3 - grj1
            [(x, y) for x in range(12, 13) for y in range(2,5)],
            #Entrada ed 3 - grj4
            [(x, y) for x in range(13, 14) for y in range(15,18)],

            #Salida ed 4 - grj4
            [(x, y) for x in range(21, 22) for y in range(2,5)],

            #Entrada ed 5 - grj1
            [(x, y) for x in range(27, 28) for y in range(7,10)],

            #Salida ed 6 - grj1
            [(x, y) for x in range(27, 28) for y in range(10,13)],
            #Entrada ed 6 - grj2
            [(x, y) for x in range(23, 24) for y in range(15,18)],

            #Salida ed 8 - grj1
            [(x, y) for x in range(13, 14) for y in range(20,23)],
            #Entrada ed 8 - grj2
            [(x, y) for x in range(4, 5) for y in range(23,26)],

            #Salida ed 9 - grj1
            [(x, y) for x in range(5, 6) for y in range(26,29)],
            #Entrada ed 9 - grj2
            [(x, y) for x in range(11, 12) for y in range(29,32)],

            #Entrada ed 10 - grj1
            [(x, y) for x in range(22, 23) for y in range(23,26)],

            #Salida ed 13 - grj1
            [(x, y) for x in range(28, 29) for y in range(26,29)],
        ]

        # Crea diccionario con direcciones permitidas
        self.direcciones_permitidas = {}
        self._populate_allowed_directions(direcciones_izquierda, 'left')
        self._populate_allowed_directions(direcciones_derecha, 'right')
        self._populate_allowed_directions(direcciones_abajo, 'down')
        self._populate_allowed_directions(direcciones_arriba, 'up')

###########################################################################################

        directions_pedestrian_up = [
            #Edificio 1 Caminos banqueta
            [(x, y) for x in range(7, 8) for y in range(3, 8)],
            [(x, y) for x in range(2, 3) for y in range(3, 8)],

            #Edificio 2 Caminos banqueta
            [(x, y) for x in range(7, 8) for y in range(10, 17)],
            [(x, y) for x in range(2, 3) for y in range(10, 17)],

            #Edificio 3 Caminos banqueta
            [(x, y) for x in range(10, 11) for y in range(3, 17)],
            [(x, y) for x in range(15, 16) for y in range(3, 17)],

            #Edificio 4 Caminos banqueta
            [(x, y) for x in range(23, 24) for y in range(3, 9)],
            [(x, y) for x in range(20, 21) for y in range(3, 9)],

            #Edificio 5 Caminos banqueta
            [(x, y) for x in range(26, 27) for y in range(3, 9)],
            [(x, y) for x in range(29, 30) for y in range(3, 9)],

            #Edificio 6 Caminos banqueta
            [(x, y) for x in range(20, 21) for y in range(11, 17)],
            [(x, y) for x in range(29, 30) for y in range(11, 17)],

            #Edificio 8 Caminos banqueta
            [(x, y) for x in range(2, 3) for y in range(21, 25)],
            [(x, y) for x in range(15, 16) for y in range(21, 25)],

            #Edificio 9 Caminos banqueta
            [(x, y) for x in range(2, 3) for y in range(27, 31)],
            [(x, y) for x in range(15, 16) for y in range(27, 31)],

            #Edificio 10 Caminos banqueta
            [(x, y) for x in range(20, 21) for y in range(21, 25)],
            [(x, y) for x in range(23, 24) for y in range(21, 25)],

            #Edificio 11 Caminos banqueta
            [(x, y) for x in range(26, 27) for y in range(21, 25)],
            [(x, y) for x in range(29, 30) for y in range(21, 25)],

            #Edificio 12 Caminos banqueta
            [(x, y) for x in range(20, 21) for y in range(27, 31)],
            [(x, y) for x in range(23, 24) for y in range(27, 31)],

            #Edificio 13 Caminos banqueta
            [(x, y) for x in range(26, 27) for y in range(27, 31)],
            [(x, y) for x in range(29, 30) for y in range(27, 31)],

            ###### Cruces arriba
            [(x, y) for x in range(2, 3) for y in range(3, 31)],
            [(x, y) for x in range(29, 30) for y in range(3, 31)],

        ]

        directions_pedestrian_down = [
            #Edificio 1 Caminos banqueta
            [(x, y) for x in range(7, 8) for y in range(1, 6)],
            [(x, y) for x in range(2, 3) for y in range(1, 6)],

            #Edificio 2 Caminos banqueta
            [(x, y) for x in range(7, 8) for y in range(8, 15)],
            [(x, y) for x in range(2, 3) for y in range(8, 15)],

            #Edificio 3 Caminos banqueta
            [(x, y) for x in range(10, 11) for y in range(1, 15)],
            [(x, y) for x in range(15, 16) for y in range(1, 15)],#

            #Edificio 4 Caminos banqueta
            [(x, y) for x in range(23, 24) for y in range(1, 7)],
            [(x, y) for x in range(20, 21) for y in range(1, 7)],

            #Edificio 5 Caminos banqueta
            [(x, y) for x in range(26, 27) for y in range(1, 7)],
            [(x, y) for x in range(29, 30) for y in range(1, 7)],

            #Edificio 6 Caminos banqueta
            [(x, y) for x in range(20, 21) for y in range(9, 15)],
            [(x, y) for x in range(29, 30) for y in range(9, 15)],

            #Edificio 8 Caminos banqueta
            [(x, y) for x in range(2, 3) for y in range(19, 23)],
            [(x, y) for x in range(15, 16) for y in range(19, 23)],

            #Edificio 9 Caminos banqueta
            [(x, y) for x in range(2, 3) for y in range(25, 29)],
            [(x, y) for x in range(15, 16) for y in range(25, 29)],

            #Edificio 10 Caminos banqueta
            [(x, y) for x in range(20, 21) for y in range(19, 23)],
            [(x, y) for x in range(23, 24) for y in range(19, 23)],

            #Edificio 11 Caminos banqueta
            [(x, y) for x in range(26, 27) for y in range(19, 23)],
            [(x, y) for x in range(29, 30) for y in range(19, 23)],

            #Edificio 12 Caminos banqueta
            [(x, y) for x in range(20, 21) for y in range(25, 29)],
            [(x, y) for x in range(23, 24) for y in range(25, 29)],

            #Edificio 13 Caminos banqueta
            [(x, y) for x in range(26, 27) for y in range(25, 29)],
            [(x, y) for x in range(29, 30) for y in range(25, 29)],

            ###### Cruces abajo
            [(x, y) for x in range(2, 3) for y in range(1, 29)],
            [(x, y) for x in range(29, 30) for y in range(1, 29)],

        ]

        directions_pedestrian_left = [
            #Edificio 1 Caminos banqueta
            [(x, y) for x in range(3, 9) for y in range(2, 3)],
            [(x, y) for x in range(3, 9) for y in range(6, 7)],

            #Edificio 2 Caminos banqueta
            [(x, y) for x in range(3, 9) for y in range(9, 10)],
            [(x, y) for x in range(3, 9) for y in range(15, 16)],

            #Edificio 3 Caminos banqueta
            [(x, y) for x in range(11, 17) for y in range(2, 3)],
            [(x, y) for x in range(11, 17) for y in range(15, 16)],

            #Edificio 4 Caminos banqueta
            [(x, y) for x in range(21, 25) for y in range(2, 3)],
            [(x, y) for x in range(21, 25) for y in range(7,8)],

            #Edificio 5 Caminos banqueta
            [(x, y) for x in range(27, 31) for y in range(2, 3)],
            [(x, y) for x in range(27, 31) for y in range(7,8)],

            #Edificio 6 Caminos banqueta
            [(x, y) for x in range(21, 31) for y in range(10, 11)],
            [(x, y) for x in range(21, 31) for y in range(15,16)],

            #Edificio 8 Caminos banqueta
            [(x, y) for x in range(3, 17) for y in range(20, 21)],
            [(x, y) for x in range(3, 17) for y in range(23, 24)],

            #Edificio 9 Caminos banqueta
            [(x, y) for x in range(3, 17) for y in range(26, 27)],
            [(x, y) for x in range(3, 17) for y in range(29, 30)],

            #Edificio 10 Caminos banqueta
            [(x, y) for x in range(21, 25) for y in range(20, 21)],
            [(x, y) for x in range(21, 25) for y in range(23, 24)],

            #Edificio 11 Caminos banqueta
            [(x, y) for x in range(27, 31) for y in range(20, 21)],
            [(x, y) for x in range(27, 31) for y in range(23, 24)],

            #Edificio 12 Caminos banqueta
            [(x, y) for x in range(21, 25) for y in range(26, 27)],
            [(x, y) for x in range(21, 25) for y in range(29, 30)],

            #Edificio 13 Caminos banqueta
            [(x, y) for x in range(27, 31) for y in range(26, 27)],
            [(x, y) for x in range(27, 31) for y in range(29, 30)],

            ###### Cruces izquierda
            [(x, y) for x in range(3, 31) for y in range(2, 3)],
            [(x, y) for x in range(3, 31) for y in range(29, 30)],

        ]

        directions_pedestrian_right = [

            #Edificio 1 Caminos banqueta
            [(x, y) for x in range(1, 7) for y in range(2, 3)],
            [(x, y) for x in range(1, 7) for y in range(6, 7)],

            #Edificio 2 Caminos banqueta
            [(x, y) for x in range(1, 7) for y in range(9, 10)],
            [(x, y) for x in range(1, 7) for y in range(15, 16)],

            #Edificio 3 Caminos banqueta
            [(x, y) for x in range(9, 15) for y in range(2, 3)],
            [(x, y) for x in range(9, 15) for y in range(15, 16)],

            #Edificio 4 Caminos banqueta
            [(x, y) for x in range(19, 23) for y in range(2, 3)],
            [(x, y) for x in range(19, 23) for y in range(7,8)],

            #Edificio 5 Caminos banqueta
            [(x, y) for x in range(25, 29) for y in range(2, 3)],
            [(x, y) for x in range(25, 29) for y in range(7,8)],

            #Edificio 6 Caminos banqueta
            [(x, y) for x in range(19, 29) for y in range(10, 11)],
            [(x, y) for x in range(19, 29) for y in range(15,16)],

            #Edificio 8 Caminos banqueta
            [(x, y) for x in range(1, 15) for y in range(20, 21)],
            [(x, y) for x in range(1, 15) for y in range(23, 24)],

            #Edificio 9 Caminos banqueta
            [(x, y) for x in range(1, 15) for y in range(26, 27)],
            [(x, y) for x in range(1, 15) for y in range(29, 30)],

            #Edificio 10 Caminos banqueta
            [(x, y) for x in range(19, 23) for y in range(20, 21)],
            [(x, y) for x in range(19, 23) for y in range(23, 24)],

            #Edificio 11 Caminos banqueta
            [(x, y) for x in range(25, 29) for y in range(20, 21)],
            [(x, y) for x in range(25, 29) for y in range(23, 24)],

            #Edificio 12 Caminos banqueta
            [(x, y) for x in range(19, 23) for y in range(26, 27)],
            [(x, y) for x in range(19, 23) for y in range(29, 30)],

            #Edificio 13 Caminos banqueta
            [(x, y) for x in range(25, 29) for y in range(26, 27)],
            [(x, y) for x in range(25, 29) for y in range(29, 30)],

            ###### Cruces derecha
            [(x, y) for x in range(1, 29) for y in range(2, 3)],
            [(x, y) for x in range(1, 29) for y in range(29, 30)],
        ]

        self.direcciones_peatones = {}
        self._populate_pedestrian_directions(directions_pedestrian_up, 'up')
        self._populate_pedestrian_directions(directions_pedestrian_down, 'down')
        self._populate_pedestrian_directions(directions_pedestrian_left, 'left')
        self._populate_pedestrian_directions(directions_pedestrian_right, 'right')


        # Crea agentes y semaforos
        self.create_pedestrians()
        self.create_traffic_lights()
        self.create_agents()

    def create_buildings(self):
        """
        Crea agentes BuildingAgent en las celdas restringidas.
        """
        for pos in self.celdas_restringidas:
            building = BuildingAgent(self.next_id(), self)
            self.grid.place_agent(building, pos)

    def create_sidewalk(self):
        """
        Crea agentes sideWalkAgent en las celdas de banquetas
        """
        for pos in self.side_walk:
            sidewalk = SideWalkAgent(self.next_id(), self)
            self.grid.place_agent(sidewalk, pos)
        
    def _populate_allowed_directions(self, direction_lists, direction):
        """
        Funcion que llena el diccionario `direcciones_permitidas` con las coordenadas válidas y sus respectivas direcciones.
        ## Argumentos
        - direction_lists (list): Lista de listas de coordenadas válidas para una dirección.
        - direction (str): Dirección asociada a las coordenadas.
        """
        for sublist in direction_lists:
            for pos in sublist:
                if pos not in self.direcciones_permitidas:
                    self.direcciones_permitidas[pos] = []
                self.direcciones_permitidas[pos].append(direction)

    def _populate_pedestrian_directions(self, direction_lists, direction_p):
        """
        Funcion que llena el diccionario `direcciones_permitidas` con las coordenadas válidas y sus respectivas direcciones.
        ## Argumentos
        - direction_lists (list): Lista de listas de coordenadas válidas para una dirección.
        - direction (str): Dirección asociada a las coordenadas.
        """
        for sublist in direction_lists:
            for pos in sublist:
                if pos not in self.direcciones_peatones:
                    self.direcciones_peatones[pos] = []
                self.direcciones_peatones[pos].append(direction_p)

    def create_pedestrians(self):
        """
        Crea agentes peatones con posiciones iniciales y destinos aleatorios dentro de las celdas de las banquetas.
        """
        for i in range(self.num_agents_p):
            # Seleccionar una posición inicial aleatoria
            start_position = self.random.choice(self.side_walk)

            # Asegurarse de que el destino sea diferente de la posición inicial
            possible_destinations = [pos for pos in self.side_walk if pos != start_position]
            destination = self.random.choice(possible_destinations)

            # Crear el agente peatón con inicio y destino
            pedestrian = PersonAgent(self, self.next_id(), start_position, destination)
            self.grid.place_agent(pedestrian, start_position)
            self.schedule.add(pedestrian)

            print(f"Peatón {pedestrian.unique_id} creado: Inicio en {start_position}, Destino en {destination}")


    def create_traffic_lights(self):
        """
        Crea y organiza los semáforos agrupados por intersección con nombres asignados.
        """
        # Diccionario para asociar nombres de cuadrantes con intersecciones
        intersections = {
            "Cuadrante 1": ([(0, 5), (1, 5)], [(3, 7), (3, 8)]),
            "Cuadrante 2": ([(16, 22), (17, 22)], [(14, 24), (14, 25)]),
            "Cuadrante 3": ([(24, 3), (25, 3)], [(27, 0), (27, 1)]),
            "Cuadrante 4": ([(30, 10), (31, 10)], [(28, 8), (28, 9)]),
            "Cuadrante 5": ([(24, 22), (25, 22)], [(27, 24), (27, 25)]),
        }

        # Iterar sobre cada cuadrante y sus intersecciones
        for quadrant_name, (ns_positions, ew_positions) in intersections.items():
            ns_lights = []
            ew_lights = []

            # Crear semáforos norte-sur
            for pos in ns_positions:
                light = Traffic_light(self, self.next_id(), pos, timer_interval=30)
                self.grid.place_agent(light, pos)
                self.schedule.add(light)
                ns_lights.append(light)

            # Crear semáforos este-oeste
            for pos in ew_positions:
                light = Traffic_light(self, self.next_id(), pos, timer_interval=30)
                self.grid.place_agent(light, pos)
                self.schedule.add(light)
                ew_lights.append(light)

            # Asignar el grupo de semáforos y nombre del cuadrante a cada semáforo
            for light in ns_lights + ew_lights:
                light.intersection_group = ns_lights + ew_lights
                light.quadrant_name = quadrant_name  # Asignar nombre del cuadrante

            # Inicializar estados
            for ns_light in ns_lights:
                ns_light.state = True  # Verde
            for ew_light in ew_lights:
                ew_light.state = False  # Rojo

            # Agregar semáforos al modelo
            self.traffic_lights.extend(ns_lights + ew_lights)

        # Imprimir información para depuración
        print(f"Cuadrante: {quadrant_name}")
        print(f"  Semáforos norte-sur: {[light.pos for light in ns_lights]}")
        print(f"  Semáforos este-oeste: {[light.pos for light in ew_lights]}")

    def create_agents(self):
    # Lista para rastrear las posiciones de los garajes ya utilizados
        used_positions = []
    
    # Itera sobre el número de agentes a crear
        for i in range(self.num_agents):
        # Selecciona aleatoriamente un garaje que no haya sido usado anteriormente
            garage = self.random.choice([g for g in self.garajes if g not in used_positions])
            # Agrega la posición del garaje a la lista de posiciones utilizadas
            used_positions.append(garage)
        
        # Selecciona aleatoriamente un destino que sea diferente al garaje seleccionado
            destination = self.random.choice([g for g in self.garajes if g != garage])
        
        # Crea una instancia del agente CarAgent con los parámetros correspondientes
            car = CarAgent(self, i, garage, None, destination)
        
        # Coloca el agente en la posición del garaje dentro de la cuadrícula del modelo
            self.grid.place_agent(car, garage)
        
            # Añade el agente al scheduler para que sea activado en cada paso de la simulación
            self.schedule.add(car)


    def step(self):
        """
        Ejecuta un paso de la simulación, activando a los agentes y sincronizando semáforos.
        """
        # Actualizar semáforos
        for light in self.traffic_lights:
            light.step()

        # Activar los agentes
        self.schedule.step()





