# Actividad Integradora
# Codigo que crea el modelo y genera los agentes y semaforos
# Autores:
# Santiago Villazón Ponce de León	A01746396
# Juan Antonio Figueroa Rodríguez	A01369043
# Iván Alexander Ramos Ramírez		A01750817
# Sebastián Antonio Almanza			A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024
# actividad_model.py

import mesa
from car_agent import CarAgent
from traffic_light import Traffic_light
from intersection import Intersection

# Nueva clase BuildingAgent
class BuildingAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = "building"  # Identificar el agente como edificio

# Clase que define el modelo de la ciudad y genera sus agentes

# Clase que define el modelo de la ciudad y genera sus agentes
class cityClass(mesa.Model):
    """
    Clase que define el ambiente (ciudad) en el que los agentes carro navegan a un destino.
    """
    def __init__(self, numberAgents=1, width=24, height=24):
        """
        Inicializa el modelo de celdas con los agentes, semaforos, altura y anchura del mapa y las celdas restringidas.
        """
        super().__init__()
        self.num_agents = numberAgents
        self.width = width
        self.height = height
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.intersections = []
        self.intersections_data = [
            {
                'positions': [
                    {'pos': (0, 4), 'orientation': 'EW'},
                    {'pos': (1, 4), 'orientation': 'EW'},
                    {'pos': (2, 5), 'orientation': 'NS'},
                    {'pos': (2, 6), 'orientation': 'NS'}
                ]
            },
            {
                'positions': [
                    {'pos': (11, 18), 'orientation': 'NS'},
                    {'pos': (11, 19), 'orientation': 'NS'},
                    {'pos': (12, 17), 'orientation': 'EW'},
                    {'pos': (13, 17), 'orientation': 'EW'}
                ]
            },
            {
                'positions': [
                    {'pos': (18, 2), 'orientation': 'EW'},
                    {'pos': (19, 2), 'orientation': 'EW'},
                    {'pos': (20, 18), 'orientation': 'NS'},
                    {'pos': (20, 19), 'orientation': 'NS'}
                ]
            },
            {
                'positions': [
                    {'pos': (21, 6), 'orientation': 'NS'},
                    {'pos': (21, 7), 'orientation': 'NS'},
                    {'pos': (18, 17), 'orientation': 'EW'},
                    {'pos': (19, 17), 'orientation': 'EW'}
                ]
            },
            {
                'positions': [
                    {'pos': (20, 0), 'orientation': 'NS'},
                    {'pos': (20, 1), 'orientation': 'NS'},
                    {'pos': (22, 8), 'orientation': 'EW'},
                    {'pos': (23, 8), 'orientation': 'EW'}
                ]
            }
        ]
        
        # Definir garajes y celdas restringidas **ANTES** de crear agentes
        self.garajes = [
            (4,4), (4, 11), (2, 8), (8, 9), (9, 2), (10, 11), (11, 6), 
            (17, 2), (20, 5), (20, 8), (18, 11), (3, 17), (10, 16), 
            (4, 20), (8, 21), (17, 17), (21, 20)
        ]
        self.celdas_restringidas = [
            (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), 
            (4, 3), (5, 2), (5, 3), (5, 4),
            (2, 7), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8), (5, 8), 
            (2, 9), (3, 9), (4, 9), (5, 9),
            (2, 10), (3, 10), (4, 10), (5, 10), (2, 11), (3, 11), (5, 11),
            (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), 
            (8, 10), (8, 11), (9, 3), (9, 4),
            (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), 
            (10, 2), (10, 3), (10, 4), (10, 5),
            (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (11, 2), 
            (11, 3), (11, 4), (11, 5), (11, 7),
            (11, 8), (11, 9), (11, 10), (11, 11), (16, 2), (16, 3), 
            (16, 4), (16, 5), (17, 3), (17, 4),
            (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), 
            (21, 4), (21, 5), (16, 8), (16, 9), 
            (16, 10), (16, 11), (17, 8), (17, 9), (17, 10), (17, 11), 
            (18, 8), (18, 9), (18, 10), (19, 8),
            (19, 9), (19, 10), (19, 11), (20, 9), (20, 10), (20, 11), 
            (21, 8), (21, 9), (21, 10), (21, 11),
            (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), 
            (8, 16), (9, 16), (11, 16), (2, 17),
            (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), 
            (10, 17), (11, 17), (2, 20), (3, 20),
            (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (11, 20), 
            (10, 20), (2, 21), (3, 21), (4, 21), 
            (5, 21), (6, 21), (7, 21), (9, 21), (10, 21), 
            (11, 21), (16, 16), (16, 17), (17, 16),
            (16, 20), (16, 21), (17, 20), (17, 21), (20, 16), 
            (20, 17), (21, 16), (21, 17), (20, 20),
            (20, 21), (21, 21), (13, 13), (14, 13), 
            (14, 14), (13, 14),
        ]
        
        # Define direcciones **DESPUÉS** de garajes y celdas restringidas
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
    
        # Crear intersecciones y semáforos
        self.create_traffic_lights()  # **LLAMADA ÚNICA**
    
        # Crear edificios
        self.create_buildings()
    
        # Crear carros
        self.create_agents()
    
    def create_buildings(self):
        """
        Crea agentes BuildingAgent en las celdas restringidas.
        """
        for pos in self.celdas_restringidas:
            building = BuildingAgent(self.next_id(), self)
            self.grid.place_agent(building, pos)
            self.schedule.add(building)
    
    def _populate_allowed_directions(self, direction_lists, direction):
        """
        Llena el diccionario `direcciones_permitidas` con las coordenadas válidas y sus respectivas direcciones.
        """
        for sublist in direction_lists:
            for pos in sublist:
                if pos not in self.direcciones_permitidas:
                    self.direcciones_permitidas[pos] = []
                self.direcciones_permitidas[pos].append(direction)
    
    def create_traffic_lights(self):
        """
        Crea y agrupa los semáforos en intersecciones.
        """
        for intersection_info in self.intersections_data:
            traffic_lights = []
    
            # Crear semáforos EW y NS
            for light_info in intersection_info['positions']:
                pos = light_info['pos']
                orientation = light_info['orientation']
                semaforo = Traffic_light(self.next_id(), self, pos, orientation)
                self.grid.place_agent(semaforo, pos)
                self.schedule.add(semaforo)
                traffic_lights.append(semaforo)
                # Agregar print para depuración
                print(f"Semáforo creado en posición {pos} con orientación {orientation}")
    
            # Crear la intersección con los semáforos agrupados
            intersection = Intersection(self.next_id(), self, traffic_lights)
            self.intersections.append(intersection)
            self.schedule.add(intersection)
    
            # Asignar la intersección a cada semáforo
            for light in traffic_lights:
                light.intersection = intersection
    
    def create_agents(self):
        """
        Crea agentes CarAgent en posiciones aleatorias (garajes) con destinos.
        """
        # Lista para rastrear las posiciones de los garajes ya utilizados
        used_positions = []
    
        for i in range(self.num_agents):
            # Seleccionar aleatoriamente un garaje no utilizado
            available_garajes = [g for g in [(5,5),(6,5)] if g not in used_positions]

            # available_garajes = [g for g in self.garajes if g not in used_positions]
            if not available_garajes:
                print(f"No hay más garajes disponibles para el agente {i}.")
                break  # Salir si no hay garajes disponibles
            garage = self.random.choice(available_garajes)
            used_positions.append(garage)
    
            # Seleccionar aleatoriamente un destino diferente al garaje
            available_destinations = [g for g in self.garajes if g != garage]
            if not available_destinations:
                print(f"No hay destinos disponibles para el agente {i}.")
                break
            destination = self.random.choice(available_destinations)
    
            # Crear el agente CarAgent
            car = CarAgent(model=self, unique_id=i, pos=garage, traffic_light=None, destination=destination)
    
            # Colocar el agente en el garaje
            self.grid.place_agent(car, garage)
            self.schedule.add(car)
    
            # Agregar print para depuración
            print(f"Carro {i} creado en garaje {garage} con destino {destination}")
    
    def step(self):
        """
        Función que realiza un paso en la simulación, activando a los agentes en orden aleatorio.
        """
        print(f"\n--- Paso {self.schedule.steps} ---")
        self.schedule.step()
