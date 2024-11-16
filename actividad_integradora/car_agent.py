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
    """
    Clase que modela un agente de tipo carro dentro de la simulación de la ciudad.
    ## Atributos:
    - model (cityClass): Referencia al modelo al que pertenece el agente.
    - unique_id (int): Identificador único del agente.
    - pos (tuple): Posición actual del agente en la cuadrícula (x, y).
    - traffic_light (Traffic_light): Referencia al semáforo asignado al agente.
    - last_direction (str): Última dirección en la que se movió el agente ('left', 'right', 'up', 'down').
    - destination (tuple): Destino del agente en la cuadrícula.
    ## Métodos:
    - __init__(self, model, unique_id, pos, traffic_light, destination): Inicializa un agente de tipo carro con una posición inicial, un semáforo asignado y un destino.
    - get_allowed_directions(self): Devuelve una lista de direcciones permitidas.
    - heuristic(self, position):Calcula la distancia de Manhattan desde una posición dada hasta el destino del agente.
    - move(self):Realiza el movimiento del agente hacia su destino, eligiendo la dirección más cercana al objetivo según la heurística y respetando las restricciones del modelo.
    - is_stop(self):Verifica si el agente debe detenerse debido a un semáforo en rojo en posiciones relevantes. Si no hay restricciones, permite el movimiento.
    - step(self):Ejecuta un paso de la simulación para el agente. 

    """
    def __init__(self, model, unique_id, pos, traffic_light, destination):
        """ 
        Inicializa un agente de tipo carro con una posición inicial, un semáforo asignado y un destino.
        ## Argumentos:
        - model (cityClass): Referencia al modelo al que pertenece el agente.
        - unique_id (int): Identificador único del agente.
        - pos (tuple): Posición actual del agente en la cuadrícula (x, y).
        - traffic_light (Traffic_light): Referencia al semáforo asignado al agente.
        - destination (tuple): Destino del agente en la cuadrícul
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.traffic_light = traffic_light
        self.last_direction = None  
        self.destination = destination 

    def get_allowed_directions(self):
        """
        Funcion que devuelve una lista de direcciones permitidas.
        """
        return self.model.direcciones_permitidas.get(self.pos, [])

    def heuristic(self, position):
        """
        Funcion que calcula la distancia de Manhattan desde una posición dada hasta el destino del agente
        """
        return abs(position[0] - self.destination[0]) + abs(position[1] - self.destination[1])

    def move(self):
        """
        Función que realiza el movimiento del agente hacia su destino, 
        eligiendo la dirección más cercana al objetivo según la heurística y respetando las restricciones del modelo.
        """
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} ha alcanzado su destino: {self.destination}")
            return  # Ya alcanzó el destino

        allowed_directions = self.get_allowed_directions()
        if not allowed_directions:
            print(f"Agente {self.unique_id} no tiene direcciones permitidas en {self.pos}")
            return  # No hay direcciones permitidas

        # Definir vectores de movimiento basados en la dirección
        direction_vectors = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }

        # Calcular la nueva posición para cada dirección permitida
        possible_moves = []
        for direction in allowed_directions:
            move_vector = direction_vectors.get(direction)
            if not move_vector:
                continue  # Dirección inválida
            new_position = (self.pos[0] + move_vector[0], self.pos[1] + move_vector[1])

            # Verificar que la nueva posición esté dentro del grid y no esté restringida
            if (0 <= new_position[0] < self.model.width and
                0 <= new_position[1] < self.model.height and
                new_position not in self.model.celdas_restringidas):

                # Evitar que el agente se mueva repetidamente al mismo garaje si no es su destino
                if new_position in self.model.garajes:
                    if new_position != self.destination:
                        continue  # Ignorar garajes que no son el destino
                    elif self.pos == new_position:
                        continue  # Ignorar si ya está en el garaje destino
                
                possible_moves.append((new_position, direction))

        if not possible_moves:
            print(f"Agente {self.unique_id} no puede moverse desde {self.pos}")
            return

        # Elegir el movimiento con la menor distancia al destino
        best_move = min(possible_moves, key=lambda x: self.heuristic(x[0]))
        new_position, direction = best_move

        # Mover al agente
        self.model.grid.move_agent(self, new_position)
        self.pos = new_position
        self.last_direction = direction
        print(f"Agente {self.unique_id} se movió a {self.pos} en dirección {self.last_direction}")

    def is_stop(self):
        """
        Función que verifica si el agente debe detenerse debido a un semáforo en rojo en posiciones relevantes. 
        Si no hay restricciones, permite el movimiento.
        """
        direction_vectors = {
            'left': [(-1, 0), (0, -1), (0, 1)],  # Oeste, Norte, Sur
            'right': [(1, 0), (0, -1), (0, 1)],  # Este, Norte, Sur
            'up': [(0, -1), (-1, 0), (1, 0)],  # Norte, Oeste, Este
            'down': [(0, 1), (-1, 0), (1, 0)],  # Sur, Oeste, Este
        }

        if not self.last_direction:
            self.move()
            return

        relevant_vectors = direction_vectors.get(self.last_direction, [])
        relevant_positions = [
            (self.pos[0] + vec[0], self.pos[1] + vec[1]) for vec in relevant_vectors
        ]

        for pos in relevant_positions:
            if not (0 <= pos[0] < self.model.width and 0 <= pos[1] < self.model.height):
                continue
            cell_contents = self.model.grid.get_cell_list_contents(pos)
            for agent in cell_contents:
                if isinstance(agent, Traffic_light) and not agent.state:  # Semáforo en rojo
                    print(f"Agente {self.unique_id} detenido por semáforo rojo en {pos}")
                    return

        self.move()
        print(f"Agente {self.unique_id} en movimiento a {self.pos}")

    def step(self):
        """
        Función que ejecuta un paso de la simulación para el agente. 
        """
        if self.pos == self.destination:
            print(f"Agente {self.unique_id} ha llegado a su destino y será eliminado.")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.is_stop()
