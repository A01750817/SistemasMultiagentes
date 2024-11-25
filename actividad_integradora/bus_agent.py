# Código que modela el agente del bus
# Autores:
# Santiago Villazón Ponce de León   A01746396
# Juan Antonio Figueroa Rodríguez   A01369043
# Iván Alexander Ramos Ramírez      A01750817
# Sebastián Antonio Almanza         A01749694
# Fecha de creación: 25/11/2024 
# Última modificación: 
# Fecha de entrega 

import mesa
from astar import Astar
from traffic_light import Traffic_light  # Importar según tu estructura de archivos

class BusAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos, ruta_Autobus):
        super().__init__(unique_id, model)
        self.type = "bus"
        self.model = model
        self.pos = pos
        self.ruta = ruta_Autobus  # Lista de paradas (posiciones)
        self.current_stop_index = 0  # Índice de la siguiente parada
        self.destination = self.ruta[self.current_stop_index]
        self.path = self.calculate_path()
        self.last_direction = None
        self.prev_cell = None
        self.priority = 1
        self.prev = None

    def calculate_path(self):
        """Calcula la ruta hacia el próximo destino usando A*."""
        if self.pos == self.destination:
            return []
        astar = Astar(self.model, self.pos, self.destination)
        path = astar.find_path()
        if path:
            print(f"Bus {self.unique_id} calculó ruta desde {self.pos} hasta {self.destination}: {path}")
            return path
        else:
            print(f"Bus {self.unique_id} no pudo calcular ruta desde {self.pos} hasta {self.destination}")
            return []

    def get_allowed_directions(self):
        """Obtiene las direcciones permitidas para el agente desde su posición actual."""
        return self.model.direcciones_permitidas.get(self.pos, [])

    def is_obstacle_ahead(self, next_pos):
        """Verifica si hay un obstáculo en la siguiente posición."""
        cell_contents = self.model.grid.get_cell_list_contents(next_pos)
        for agent in cell_contents:
            if agent is not self and hasattr(agent, 'type') and agent.type in ['car', 'bus', 'building']:
                return True
        return False

    def is_stop_light(self):
        """Detiene al bus si encuentra un semáforo en rojo."""
        if not self.last_direction:
            return False
        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }
        move_vector = direction_vectors.get(self.last_direction)
        if not move_vector:
            return False
        front_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])
        if not (0 <= front_position[0] < self.model.width and 0 <= front_position[1] < self.model.height):
            return False
        cell_contents = self.model.grid.get_cell_list_contents(front_position)
        for agent in cell_contents:
            if isinstance(agent, Traffic_light) and not agent.state:
                print(f"Bus {self.unique_id} detenido por semáforo rojo en {front_position}")
                return True
        return False

    def move(self):
        """Realiza el movimiento siguiendo la ruta calculada."""
        if not self.path:
            self.path = self.calculate_path()
            if not self.path:
                return  # No hay camino disponible
        next_pos = self.path[0]

        # Determinar la dirección del movimiento
        dx = next_pos[0] - self.pos[0]
        dy = next_pos[1] - self.pos[1]
        if dx == -1:
            self.last_direction = 'left'
        elif dx == 1:
            self.last_direction = 'right'
        elif dy == -1:
            self.last_direction = 'up'
        elif dy == 1:
            self.last_direction = 'down'

        # Verificar semáforos
        if self.is_stop_light():
            return  # Detenerse en semáforo rojo

        # Verificar obstáculos
        if self.is_obstacle_ahead(next_pos):
            print(f"Bus {self.unique_id} no puede moverse a {next_pos}; posición ocupada.")
            return  # Esperar hasta que el camino esté libre

        # Mover el bus
        self.model.grid.move_agent(self, next_pos)
        self.pos = next_pos
        self.path.pop(0)
        print(f"Bus {self.unique_id} se movió a {self.pos}")

    def step(self):
        """Comportamiento del bus en cada paso."""
        if self.pos == self.destination:
            print(f"Bus {self.unique_id} ha llegado a la parada {self.destination}")
            self.current_stop_index += 1
            if self.current_stop_index >= len(self.ruta):
                self.current_stop_index = 0  # Reiniciar la ruta
            self.destination = self.ruta[self.current_stop_index]
            self.path = self.calculate_path()
        else:
            self.move()