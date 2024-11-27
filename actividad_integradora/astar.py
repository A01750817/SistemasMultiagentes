from queue import PriorityQueue

class Astar:
    def __init__(self, model, start, end):
        """
        Inicializa el algoritmo A*.
        :param model: La referencia al modelo de la simulación.
        :param start: Posición inicial (x, y).
        :param end: Posición final (x, y).
        """
        self.model = model
        self.start = start
        self.end = end
        self.g_score = {}
        self.f_score = {}
        self.open_set = PriorityQueue()
        self.open_set.put((0, start))
        self.came_from = {}
        self.g_score[start] = 0
        self.f_score[start] = self.heuristic(start, end)

    def heuristic(self, a, b):
        """Calcula la distancia Manhattan entre dos puntos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position):
        neighbors = []
        x, y = position
        potential_neighbors = [
            ((x - 1, y), 'left'), 
            ((x + 1, y), 'right'), 
            ((x, y - 1), 'up'), 
            ((x, y + 1), 'down')
        ]

        allowed_directions = self.model.direcciones_permitidas.get(position, [])

        for neighbor, direction in potential_neighbors:
            if (0 <= neighbor[0] < self.model.width and
                0 <= neighbor[1] < self.model.height and
                direction in allowed_directions):
                content = self.model.grid.get_cell_list_contents(neighbor)
                if not any(hasattr(agent, 'type') and agent.type in ['building'] for agent in content):
                    neighbors.append(neighbor)

        return neighbors
    
    def get_pedestrian_neighbors(self, position):
        """Obtiene los vecinos válidos específicamente para peatones."""
        neighbors = []
        x, y = position
        potential_neighbors = [
            ((x - 1, y), 'left'), 
            ((x + 1, y), 'right'), 
            ((x, y - 1), 'up'), 
            ((x, y + 1), 'down')
        ]

        allowed_directions = self.model.direcciones_peatones.get(position, [])

        for neighbor, direction in potential_neighbors:
            if (0 <= neighbor[0] < self.model.width and
                0 <= neighbor[1] < self.model.height and
                direction in allowed_directions):
                content = self.model.grid.get_cell_list_contents(neighbor)
                # Evitar celdas ocupadas por otros peatones o edificios
                if not any(hasattr(agent, 'type') and agent.type in ['building', 'pedestrian'] for agent in content):
                    neighbors.append(neighbor)

        return neighbors

    def reconstruct_path(self, current):
        """Reconstruye el camino desde la posición final hasta la inicial."""
        path = []
        while current in self.came_from:
            path.append(current)
            current = self.came_from[current]
        path.reverse()
        return path

    def find_path(self):
        while not self.open_set.empty():
            _, current = self.open_set.get()

            if current == self.end:
                return self.reconstruct_path(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g_score[current] + 1

                if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, self.end)
                    self.f_score[neighbor] = f_score
                    self.open_set.put((f_score, neighbor))

        return []
    
    def find_path_ped(self):
        """
        Encuentra el camino utilizando el algoritmo A*.
        :return: Una lista con el camino si existe, o una lista vacía si no.
        """
        while not self.open_set.empty():
            _, current = self.open_set.get()

            if current == self.end:
                return self.reconstruct_path(current)

            for neighbor in self.get_pedestrian_neighbors(current):
                tentative_g_score = self.g_score[current] + 1

                if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, self.end)
                    self.f_score[neighbor] = f_score
                    self.open_set.put((f_score, neighbor))

        # Mensaje cuando no hay camino válido
        print(f"ERROR: No se encontró una ruta válida de {self.start} a {self.end}.")
        return []

