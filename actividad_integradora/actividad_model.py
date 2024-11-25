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

# Nueva clase BuildingAgent
class BuildingAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "building"  # Identificar el agente como edificio

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
    def __init__(self, numberAgents=1, width=24, height=24):
        """
        Inicializa el modelo de celdas con los agentes, semaforos, altura y anchura del mapa y las celdas restringidas.
        ## Argumentos:
        - numberAgents (int): Número de agentes en la simulación.
        - width (int): Ancho de la cuadrícula de la ciudad.
        - height (int): Alto de la cuadrícula de la ciudad.
        """
        super().__init__()
        self.num_agents = numberAgents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.traffic_lights = []
        self.garajes = [(4,4), (4, 11), (2, 8), (8, 9), (9, 2), (10, 11), (11, 6), (17, 2), (20, 5), (20, 8), 
           (18, 11), (3, 17), (10, 16), (4, 20), (8, 21), (17, 17), (21, 20)]
        self.celdas_restringidas = [
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

        # Define direcciones
        direcciones_izquierda = [
            [(x, y) for x in range(25) for y in range(0,2)],
            [(x, y) for x in range(2,8) for y in range(5,7)],
            [(x, y) for x in range(2,14) for y in range(12,14)],
            [(x, y) for x in range(16,24) for y in range(12,14)],
            [(x, y) for x in range(16,24) for y in range(18,20)],
            [(x, y) for x in range(13, 17) for y in range(12, 13)],
            [(2, 8), (8, 9), (12, 6), (18, 2), (20, 5), (18, 17), (22, 20)]
        ]

        direcciones_derecha = [
            [(x, y) for x in range(0,12) for y in range(14,16)],
            [(x, y) for x in range(0,12) for y in range(18,20)],
            [(x, y) for x in range(14,22) for y in range(14,16)],
            [(x, y) for x in range(14,22) for y in range(6,8)],
            [(x, y) for x in range(-1, 24) for y in range(22,24)],
            [(x, y) for x in range(11, 15) for y in range(15, 16)],
            [(1, 8), (7, 9), (11, 6), (17, 2), (19, 5), (17, 17), (21, 20)]
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

        # Crea diccionario con direcciones permitidas
        self.direcciones_permitidas = {}
        self._populate_allowed_directions(direcciones_izquierda, 'left')
        self._populate_allowed_directions(direcciones_derecha, 'right')
        self._populate_allowed_directions(direcciones_abajo, 'down')
        self._populate_allowed_directions(direcciones_arriba, 'up')

        # Crea agentes y semaforos
        self.create_traffic_lights()
        self.create_agents()

    def create_buildings(self):
        """
        Crea agentes BuildingAgent en las celdas restringidas.
        """
        for pos in self.celdas_restringidas:
            building = BuildingAgent(self.next_id(), self)
            self.grid.place_agent(building, pos)


        
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

    def create_traffic_lights(self):
        """
        Crea y organiza los semáforos agrupados por intersección con nombres asignados.
        """
        # Diccionario para asociar nombres de cuadrantes con intersecciones
        intersections = {
            "Cuadrante 1": ([(0, 4), (1, 4)], [(2, 5), (2, 6)]),
            "Cuadrante 2": ([(12, 17), (13, 17)], [(11, 18), (11, 19)]),
            "Cuadrante 3": ([(18, 2), (19, 2)], [(20, 0), (20, 1)]),
            "Cuadrante 4": ([(22, 8), (23, 8)], [(21, 6), (21, 7)]),
            "Cuadrante 5": ([(18, 17), (19, 17)], [(20, 18), (20, 19)]),
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
            # Asegúrate de que el garage es válido (dentro del rango y no restringido)
            if self.grid.out_of_bounds(garage) or garage in self.celdas_restringidas:
                continue
            
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




