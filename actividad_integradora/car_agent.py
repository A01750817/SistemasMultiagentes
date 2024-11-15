import mesa
from traffic_light import Traffic_light  # Importando Traffic_light

class CarAgent(mesa.Agent):
    """
    Clase que modela un carro como agente
    """
    def __init__(self, model, unique_id, pos, traffic_light):
        super().__init__(unique_id, model)
        self.pos = pos
        self.traffic_light = traffic_light
        self.last_direction = None  # Almacenar la última dirección de movimiento

    def get_allowed_directions(self):
        """
        Obtiene las direcciones permitidas en la posición actual.
        """
        return self.model.direcciones_permitidas.get(self.pos, [])

    def move(self):
        allowed_directions = self.get_allowed_directions()
        if not allowed_directions:
            print(f"Agente {self.unique_id} no tiene direcciones permitidas en {self.pos}")
            return  # No hay direcciones permitidas

        # Elegir una dirección al azar entre las permitidas
        direction = self.random.choice(allowed_directions)

        # Definir vectores de movimiento basados en la dirección
        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }

        move_vector = direction_vectors.get(direction)
        if not move_vector:
            print(f"Agente {self.unique_id} tiene una dirección inválida: {direction}")
            return  # Dirección inválida

        new_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])

        # Verificar que la nueva posición esté dentro del grid
        if not (0 <= new_position[0] < self.model.width and 0 <= new_position[1] < self.model.height):
            print(f"Agente {self.unique_id} intenta moverse fuera del grid a {new_position}")
            return

        # Verificar que la nueva posición no esté restringida
        if new_position in self.model.celdas_restringidas:
            print(f"Agente {self.unique_id} intenta moverse a una celda restringida: {new_position}")
            return

        # Verificar si la celda ya está ocupada por otro agente
        cell_contents = self.model.grid.get_cell_list_contents(new_position)
        for agent in cell_contents:
            if isinstance(agent, CarAgent):
                print(f"Agente {self.unique_id} encuentra otro agente en {new_position}, no puede moverse")
                return

        # Mover al agente
        self.model.grid.move_agent(self, new_position)
        self.pos = new_position
        self.last_direction = direction  # Actualizar la última dirección de movimiento
        print(f"Agente {self.unique_id} se movió a {self.pos}")

    def is_stop(self):
        # Definir los puntos relevantes según la dirección de movimiento
        direction_vectors = {
            'left': [(-1, 0), (0, -1), (0, 1)],  # Oeste, Norte, Sur
            'right': [(1, 0), (0, -1), (0, 1)],  # Este, Norte, Sur
            'up': [(0, -1), (-1, 0), (1, 0)],  # Norte, Oeste, Este
            'down': [(0, 1), (-1, 0), (1, 0)],  # Sur, Oeste, Este
        }

        if not self.last_direction:
            # Si no hay dirección previa (agente recién colocado), moverse sin restricciones
            self.move()
            return

        # Obtener los vectores relevantes para la dirección actual
        relevant_vectors = direction_vectors.get(self.last_direction, [])
        relevant_positions = [
            (self.pos[0] + vec[0], self.pos[1] + vec[1]) for vec in relevant_vectors
        ]

        # Verificar si hay un semáforo en rojo en las posiciones relevantes
        for pos in relevant_positions:
            if not (0 <= pos[0] < self.model.width and 0 <= pos[1] < self.model.height):
                continue  # Ignorar posiciones fuera del grid
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            for agent in cell_contents:
                if isinstance(agent, Traffic_light) and not agent.state:  # Semáforo en rojo
                    print(f"Agente {self.unique_id} detenido por semáforo rojo en {pos}")
                    return

        # Si no hay semáforos en rojo en las posiciones relevantes, moverse
        self.move()
        print(f"Agente {self.unique_id} en movimiento a {self.pos}")

    def step(self):
        self.is_stop()