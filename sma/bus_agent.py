# bus_agent.py

import mesa
from traffic_light import Traffic_light   # Importando Traffic_light
from astar import Astar
import random

class BusAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos, traffic_light, ruta_Autobus):
        super().__init__(unique_id, model)
        self.type = "bus"
        self.model = model
        self.traffic_light = traffic_light
        self.numeroPeatones = 0
        self.passengers = []  # Lista para almacenar pasajeros
        self.ruta = ruta_Autobus  # Lista de paradas (tuplas de coordenadas)
        self.visited_stops = set()  # Conjunto para rastrear paradas visitadas
        self.current_stop_index = 0  # Índice de la siguiente parada
        self.destination = self.ruta[self.current_stop_index]
        self.pos = pos  # Asignar la posición inicial
        self.path = self.calculate_path()
        self.last_direction = None
        self.prev_cell = None
        self.priority = 1
        self.prev = None
        self.stop_counter = 0

    def calculate_path(self):
        """Calcula la ruta usando A*."""
        astar = Astar(self.model, self.pos, self.destination)
        return astar.find_path()

    def get_allowed_directions(self):
        """Obtiene las direcciones permitidas para el agente desde su posición actual."""
        return self.model.direcciones_permitidas.get(self.pos, [])

    def __is_there_a_vehicle(self, next_cell):
        """Verifica si hay un vehículo (carro o bus) en la siguiente celda."""
        if next_cell != self.prev_cell:
            content = self.model.grid.get_cell_list_contents(next_cell)
            for agent in content:
                if agent.type in ['car', 'bus']:
                    return True
        return False

    def __give_priority(self):
        """Asigna prioridad al bus basado en su posición actual."""
        x, y = self.pos
        priority = 1
        content = self.model.grid.get_cell_list_contents(self.pos)
        for agent in content:
            if agent.type == 'parking':
                priority = 3
                break
        else:
            if (x < 2 or x > self.model.width - 3) or \
            (y < 2 or y > self.model.height - 3):
                priority = 2
            else:
                priority = 1
        self.priority = priority
        
    def handle_stop(self):
        """Gestiona el embarque y desembarque de pasajeros."""
        # Desembarcar pasajeros
        for passenger in self.passengers.copy():
            # Decidir si el pasajero se baja en esta parada
            decision = True  # Implementa tu lógica de decisión
            if decision:
                passenger.on_bus = False
                passenger.bus = None
                passenger.pos = self.pos  # Colocar al pasajero en la posición actual del bus
                self.model.grid.place_agent(passenger, self.pos)
                self.model.schedule.add(passenger)
                self.passengers.remove(passenger)
                print(f"Peatón {passenger.unique_id}: Se bajó del autobús {self.unique_id} en {self.pos}.")

        # Embarcar pasajeros en las celdas adyacentes a la parada (bus)
        adjacent_positions = self.get_adjacent_positions()
        for pos in adjacent_positions:
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            for agent in cell_contents:
                if getattr(agent, "type", None) == "pedestrian" and agent.waiting_at_bus_stop:
                    # Subir al pasajero al autobús
                    agent.on_bus = True
                    agent.bus = self
                    self.passengers.append(agent)
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
                    print(f"Peatón {agent.unique_id}: Se subió al autobús {self.unique_id} desde {pos}.")

    def __can_change_to(self):
        """Determina qué direcciones puede tomar el bus para cambiar de carril."""
        direction = None
        cell = self.model.grid.get_cell_list_contents(self.pos)
        for agent in cell:
            if agent.type == 'road':
                direction = agent.direction
                break
        if direction == "right":
            directions = [(self.pos[0], self.pos[1] + 1),
                          (self.pos[0], self.pos[1] - 1),
                          (self.pos[0] + 1, self.pos[1])]
        elif direction == "left":
            directions = [(self.pos[0], self.pos[1] + 1),
                          (self.pos[0], self.pos[1] - 1),
                          (self.pos[0] - 1, self.pos[1])]
        elif direction == "up":
            directions = [(self.pos[0] + 1, self.pos[1]),
                          (self.pos[0] - 1, self.pos[1]),
                          (self.pos[0], self.pos[1] + 1)]
        elif direction == "down":
            directions = [(self.pos[0] + 1, self.pos[1]),
                          (self.pos[0] - 1, self.pos[1]),
                          (self.pos[0], self.pos[1] - 1)]
        else:
            directions = []

        available_directions = []
        for cell in directions:
            if not self.model.grid.out_of_bounds(cell):
                content = self.model.grid.get_cell_list_contents(cell)
                if not any(agent.type in ['building', 'parking', 'car', 'bus'] for agent in content):
                    available_directions.append(cell)
        return available_directions

    def __calculate_prev(self):
        """Asigna la dirección previa al bus."""
        cell = self.model.grid.get_cell_list_contents(self.pos)
        direction = None
        for agent in cell:
            if agent.type in ['road', 'light']:
                direction = agent.direction
                break
        if direction:
            if direction in ['intersection', 'light_vertical', 'light_horizontal']:
                return False
            self.prev = direction
            return True
        return False
    
    def find_next_stop(self):
        """Encuentra la siguiente parada con la menor distancia de camino."""
        unvisited_stops = [stop for stop in self.model.bus_stops if stop not in self.visited_stops]

        if not unvisited_stops:
            self.visited_stops = set()
            unvisited_stops = self.model.bus_stops.copy()

        min_distance = float('inf')
        closest_stop = None
        best_path = []

        for stop in unvisited_stops:
            astar = Astar(self.model, self.pos, stop)
            path = astar.find_path()
            if path:
                distance = len(path)
                if distance < min_distance:
                    min_distance = distance
                    closest_stop = stop
                    best_path = path

        if closest_stop:
            print(f"Agente bus {self.unique_id} selecciona la siguiente parada: {closest_stop} con una distancia de {min_distance}")
            return closest_stop
        else:
            print(f"Agente bus {self.unique_id} no encontró una parada accesible.")
            return None
        
    def __change_lanes(self):
        """El bus cambia de carril si es posible."""
        cells_move = self.__can_change_to()
        if cells_move:
            for neighbor in cells_move:
                if self.prev_cell != neighbor:
                    if not self.model.grid.out_of_bounds(neighbor):
                        if not self.__is_there_a_obstacle(neighbor):
                            self.__calculate_prev()
                            self.prev_cell = self.pos
                            self.model.grid.move_agent(self, neighbor)
                            self.path = self.calculate_path()
                            print(f"Agente bus {self.unique_id} cambió de carril a {self.pos}")
                            return True
        return False

    def __is_there_a_obstacle(self, next_cell):
        """Verifica si hay un obstáculo en la siguiente celda."""
        content = self.model.grid.get_cell_list_contents(next_cell)
        for agent in content:
            if agent.type in ['building', 'parking', 'car', 'bus']:
                return True
        return False
    
    def get_adjacent_positions(self):
        """Devuelve una lista de posiciones adyacentes al autobús."""
        x, y = self.pos
        adjacent_positions = [
            (x - 1, y), (x + 1, y),       # izquierda y derecha
            (x, y - 1), (x, y + 1),       # arriba y abajo
            (x - 1, y - 1), (x - 1, y + 1),  # diagonales superiores
            (x + 1, y - 1), (x + 1, y + 1)   # diagonales inferiores
        ]
        # Filtrar posiciones que estén dentro de los límites del grid
        valid_positions = [
            pos for pos in adjacent_positions
            if 0 <= pos[0] < self.model.grid.width and 0 <= pos[1] < self.model.grid.height
        ]
        return valid_positions

    def move(self):
        """Realiza el movimiento del agente siguiendo la ruta calculada."""
        if self.stop_counter > 0:
            self.stop_counter -= 1
            print(f"Agente bus {self.unique_id} está esperando en la parada {self.destination}. Tiempo restante: {self.stop_counter}")
            if self.stop_counter == 0 and self.destination:
                # Procesar desembarque y embarque
                self.handle_stop()
                # Después de esperar, buscar la siguiente parada y calcular la ruta
                self.visited_stops.add(self.destination)
                self.destination = self.find_next_stop()
                if self.destination:
                    self.path = self.calculate_path()
                    print(f"Agente bus {self.unique_id} comienza a moverse hacia la siguiente parada {self.destination}")
            return

        if self.destination is None:
            # No hay una parada válida para dirigirse
            print(f"Agente bus {self.unique_id} no tiene una parada de destino válida.")
            return

        if self.pos == self.destination:
            print(f"Autobús {self.unique_id}: Llegó a la parada {self.destination}.")
            self.stop_counter = 20  # El autobús se detiene por 20 pasos
            self.handle_stop()
            # Actualiza las paradas visitadas y busca la siguiente parada
            self.visited_stops.add(self.destination)
            self.destination = self.find_next_stop()
            if self.destination:
                self.path = self.calculate_path()
            return  # El autobús está detenido, no continúa moviéndose este paso

        if not self.path or self.pos != self.path[0]:
            self.path = self.calculate_path()

        if not self.path:
            print(f"Agente bus {self.unique_id} no tiene ruta válida desde {self.pos} a {self.destination}")
            return

        next_step = self.path.pop(0)

        if not self.__is_there_a_vehicle(next_step):
            allowed_directions = self.get_allowed_directions()
            direction_vectors = {
                'left': (-1, 0),
                'right': (1, 0),
                'up': (0, -1),
                'down': (0, 1),
            }
            for direction, vector in direction_vectors.items():
                target_position = (self.pos[0] + vector[0], self.pos[1] + vector[1])
                if target_position == next_step and direction in allowed_directions:
                    self.prev_cell = self.pos
                    self.__give_priority()
                    self.__calculate_prev()
                    self.model.grid.move_agent(self, next_step)
                    self.pos = next_step
                    self.last_direction = direction
                    print(f"Agente bus {self.unique_id} se movió a {self.pos} en dirección {direction}")
                    print(f"Prioridad del agente bus {self.unique_id}: {self.priority}")
                    return

        if not self.__change_lanes():
            print(f"Agente bus {self.unique_id} no puede moverse desde {self.pos} ni cambiar de carril.")
            
    def is_stop(self):
        """Determina si el bus debe detenerse por un semáforo en rojo."""
        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }

        if not self.last_direction:
            return False

        move_vector = direction_vectors.get(self.last_direction)
        if not move_vector:
            return False

        front_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])

        if not (0 <= front_position[0] < self.model.grid.width and 0 <= front_position[1] < self.model.grid.height):
            return False

        cell_contents = self.model.grid.get_cell_list_contents(front_position)
        for agent in cell_contents:
            if isinstance(agent, Traffic_light) and not agent.state:
                print(f"Agente bus {self.unique_id} detenido por semáforo rojo en {front_position}")
                return True

        return False

    def manhattan_distance(self, a, b):
        """Calcula la distancia Manhattan entre dos puntos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_next_stop(self):
        """Encuentra la siguiente parada más cercana que no haya sido visitada."""
        unvisited_stops = [stop for stop in self.model.bus_stops if stop not in self.visited_stops]

        if not unvisited_stops:
            self.visited_stops = set()
            unvisited_stops = self.model.bus_stops.copy()

        closest_stop = min(unvisited_stops, key=lambda stop: self.manhattan_distance(self.pos, stop))
        return closest_stop

    def step(self):
        """Define el comportamiento del agente en cada paso."""
        if self.is_stop():
            return

        self.move()