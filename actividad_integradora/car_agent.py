# Actividad Integradora
# Codigo que modela el agente del auto
# Autores:
# Santiago Villazón Ponce de León	A01746396
# Juan Antonio Figueroa Rodríguez	A01369043
# Iván Alexander Ramos Ramírez		A01750817
# Sebastián Antonio Almanza			A01749694
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

    def calculate_path(self):
        """Calcula la ruta usando A*."""
        astar = Astar(self.model, self.pos, self.destination)
        return astar.find_path()

    def get_allowed_directions(self):
        return self.model.direcciones_permitidas.get(self.pos, [])

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

        # Comprobar si el siguiente paso está permitido por las direcciones y no es un edificio
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
                self.model.grid.move_agent(self, next_step)
                self.pos = next_step
                self.last_direction = direction
                print(f"Agente {self.unique_id} se movió a {self.pos} en dirección {direction}")
                return

        print(f"Agente {self.unique_id} no puede moverse desde {self.pos}")

    def is_stop(self):
        """Detiene al agente si encuentra un semáforo en rojo."""
        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }

        if not self.last_direction:
            self.move()
            return

        move_vector = direction_vectors.get(self.last_direction)
        if not move_vector:
            self.move()
            return

        front_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])

        if not (0 <= front_position[0] < self.model.width and 0 <= front_position[1] < self.model.height):
            self.move()
            return

        cell_contents = self.model.grid.get_cell_list_contents(front_position)
        for agent in cell_contents:
            if isinstance(agent, Traffic_light) and not agent.state:
                print(f"Agente {self.unique_id} detenido por semáforo rojo en {front_position}")
                return

        self.move()

    def step(self):
        if self.path is None:
            print(f"Agente {self.unique_id} calculando ruta desde {self.pos} hacia {self.destination}")
            self.calculate_path()
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} alcanzó su destino en {self.destination}")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        elif self.path:
            next_step = self.path.pop(0)
            print(f"Agente {self.unique_id} se mueve de {self.pos} a {next_step}")
            self.model.grid.move_agent(self, next_step)