# Actividad Integradora
# Codigo que modela el agente del auto
# Autores:
# Santiago Villazón Ponce de León   A01746396
# Juan Antonio Figueroa Rodríguez   A01369043
# Iván Alexander Ramos Ramírez      A01750817
# Sebastián Antonio Almanza         A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024
import mesa
from astar import Astar
from traffic_light import Traffic_light  # Importando Traffic_light

class CarAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos, traffic_light, destination):
        super().__init__(unique_id, model)
        self.type = "car"  # Atributo que identifica al agente como carro
        self.pos = pos
        self.traffic_light = traffic_light
        self.destination = destination
        self.path = self.calculate_path()
        self.current_step = 0
        self.last_direction = None  # Inicializa last_direction para evitar errores
        self.prev_cell = None  # Celda anterior para referencia
        self.priority = 1  # Prioridad inicial del coche (1 = más baja)
        self.prev = None  # Última dirección calculada

    def calculate_path(self):
        """Calcula la ruta usando A*."""
        astar = Astar(self.model, self.pos, self.destination)
        return astar.find_path()

    def get_allowed_directions(self):
        """Obtiene las direcciones permitidas para el agente desde su posición actual."""
        return self.model.direcciones_permitidas.get(self.pos, [])

    def __is_there_a_car(self, next_cell):
        """Checks whether there is a car in next cell."""
        if next_cell != self.prev_cell:  # Evitar conflictos con la celda anterior
            content = self.model.grid.get_cell_list_contents(next_cell)
            for agent in content:
                if agent.type == 'car':  # Verifica si hay un coche en la celda
                    return True
        return False

    def __is_there_a_obstacle(self, next_cell):
        """Checks whether there is an obstacle in next cell."""
        content = self.model.grid.get_cell_list_contents(next_cell)
        for agent in content:
            if agent.type in ['car', 'building', 'parking']:
                return True
        return False

    def __give_priority(self):
        """Asigna prioridad al coche basado en su posición actual."""
        x, y = self.pos
        priority = 1  # Prioridad más baja (por defecto)
        content = self.model.grid.get_cell_list_contents(self.pos)

        # Prioridad alta si está en un lugar de estacionamiento
        for agent in content:
            if agent.type == 'parking':
                priority = 3  # Prioridad más alta
                break
        else:
            # Prioridad media si está en una carretera principal
            if (x < 2 or x > self.model.width - 3) or \
               (y < 2 or y > self.model.height - 3):
                priority = 2  # Prioridad media
            # Prioridad baja si está en una carretera central
            else:
                priority = 1  # Prioridad más baja
        self.priority = priority

    def __can_change_to(self):
        """Determina qué direcciones puede tomar el coche para cambiar de carril."""
        direction = None
        cell = self.model.grid.get_cell_list_contents(self.pos)

        # Obtiene la dirección actual de la celda
        for agent in cell:
            if agent.type == 'road':
                direction = agent.direction
                break

        # Define las direcciones permitidas basadas en la dirección actual
        if direction == "right":
            direction = [(self.pos[0], self.pos[1] + 1),  # Abajo
                         (self.pos[0], self.pos[1] - 1),  # Arriba
                         (self.pos[0] + 1, self.pos[1])]  # Derecha
        elif direction == "left":
            direction = [(self.pos[0], self.pos[1] + 1),  # Abajo
                         (self.pos[0], self.pos[1] - 1),  # Arriba
                         (self.pos[0] - 1, self.pos[1])]  # Izquierda
        elif direction == "up":
            direction = [(self.pos[0] + 1, self.pos[1]),  # Derecha
                         (self.pos[0] - 1, self.pos[1]),  # Izquierda
                         (self.pos[0], self.pos[1] + 1)]  # Arriba
        elif direction == "down":
            direction = [(self.pos[0] + 1, self.pos[1]),  # Derecha
                         (self.pos[0] - 1, self.pos[1]),  # Izquierda
                         (self.pos[0], self.pos[1] - 1)]  # Abajo
        else:
            direction = []  # No hay direcciones disponibles

        # Filtra las celdas disponibles para evitar obstáculos
        available_directions = []
        for cell in direction:
            if not self.model.grid.out_of_bounds(cell):  # Verifica si la celda está dentro del grid
                content = self.model.grid.get_cell_list_contents(cell)
                if not any(agent.type in ['building', 'parking', 'car'] for agent in content):
                    available_directions.append(cell)
        return available_directions

    def __calculate_prev(self):
        """Assigns previous direction to car."""
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

    def __change_lanes(self):
        """Car changes lanes if it is available."""
        cells_move = self.__can_change_to()
        if cells_move:
            for neighbor in cells_move:
                if self.prev_cell != neighbor:
                    if not self.model.grid.out_of_bounds(neighbor):
                        if not self.__is_there_a_obstacle(neighbor):
                            self.__calculate_prev()
                            self.prev_cell = self.pos
                            self.model.grid.move_agent(self, neighbor)
                            astar = Astar(self.model, self.pos, self.destination)
                            self.path = astar.find_path()
                            print(f"Agente {self.unique_id} cambió de carril a {self.pos}")
                            return True
        return False

    def move(self):
        """Realiza el movimiento del agente siguiendo la ruta calculada."""
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} ha alcanzado su destino: {self.destination}")
            return 

        if not self.path or self.pos != self.path[0]:
            self.path = self.calculate_path()

        if not self.path:
            print(f"Agente {self.unique_id} no tiene ruta válida desde {self.pos}")
            return

        next_step = self.path.pop(0)

        # Verificar si el siguiente paso está permitido y no ocupado por otro agente
        if not self.__is_there_a_car(next_step):  # Verifica si la celda no tiene otro coche
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
                    self.prev_cell = self.pos  # Actualiza la celda anterior
                    self.__give_priority()  # Actualiza la prioridad antes de moverse
                    self.__calculate_prev()  # Actualiza la dirección previa
                    self.model.grid.move_agent(self, next_step)
                    self.pos = next_step
                    self.last_direction = direction
                    print(f"Agente {self.unique_id} se movió a {self.pos} en dirección {direction}")
                    print(f"Prioridad del agente {self.unique_id}: {self.priority}")
                    return

        # Si no puede moverse, intenta cambiar de carril
        if not self.__change_lanes():
            print(f"Agente {self.unique_id} no puede moverse desde {self.pos} ni cambiar de carril.")

    def is_stop(self):
        """Detiene al agente si encuentra un semáforo en rojo."""
        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }

        # Si no hay una dirección previa, calcula el siguiente paso
        if not self.last_direction:
            self.move()
            return

        # Calcula la posición frente al agente basada en la dirección actual
        move_vector = direction_vectors.get(self.last_direction)
        if not move_vector:
            self.move()
            return

        front_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])

        # Si la posición frente al agente está fuera del rango del grid
        if not (0 <= front_position[0] < self.model.width and 0 <= front_position[1] < self.model.height):
            self.move()
            return

        # Verifica el contenido de la celda frente al agente
        cell_contents = self.model.grid.get_cell_list_contents(front_position)
        for agent in cell_contents:
            # Si hay un semáforo y está en rojo, detén al agente
            if isinstance(agent, Traffic_light) and not agent.state:
                print(f"Agente {self.unique_id} detenido por semáforo rojo en {front_position}")
                return

        # Si no hay un semáforo en rojo, el agente puede moverse
        self.move()

    def step(self):
        """Define el comportamiento del agente en cada paso."""
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} alcanzó su destino en {self.destination}")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            # Primero verifica si debe detenerse en un semáforo
            self.is_stop()

