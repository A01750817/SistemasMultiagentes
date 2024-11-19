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
from traffic_light import Traffic_light  # Importando Traffic_light

class CarAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos, traffic_light, destination):
        super().__init__(unique_id, model)
        self.pos = pos
        self.traffic_light = traffic_light
        self.last_direction = None  
        self.destination = destination 

    def get_allowed_directions(self):
        return self.model.direcciones_permitidas.get(self.pos, [])

    def heuristic(self, position):
        return abs(position[0] - self.destination[0]) + abs(position[1] - self.destination[1])

    def move(self):
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} ha alcanzado su destino: {self.destination}")
            return 

        allowed_directions = self.get_allowed_directions()
        if not allowed_directions:
            print(f"Agente {self.unique_id} no tiene direcciones permitidas en {self.pos}")
            return 

        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }

        possible_moves = []
        for direction in allowed_directions:
            move_vector = direction_vectors.get(direction)
            if not move_vector:
                continue  
            new_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])

            if (0 <= new_position[0] < self.model.width and
                0 <= new_position[1] < self.model.height and
                new_position not in self.model.celdas_restringidas):

                if new_position in self.model.garajes:
                    if new_position != self.destination:
                        continue  
                    elif self.pos == new_position:
                        continue  

                possible_moves.append((new_position, direction))

        if not possible_moves:
            print(f"Agente {self.unique_id} no puede moverse desde {self.pos}")
            return

        best_move = min(possible_moves, key=lambda x: self.heuristic(x[0]))
        new_position, direction = best_move

        self.model.grid.move_agent(self, new_position)
        self.pos = new_position
        self.last_direction = direction
        print(f"Agente {self.unique_id} se movió a {self.pos} en dirección {self.last_direction}")

    def is_stop(self):
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
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} ha llegado a su destino y será eliminado.")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.is_stop()
