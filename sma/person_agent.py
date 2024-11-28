import mesa
from astar import Astar

class PersonAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos, destination):
        super().__init__(unique_id, model)
        self.type = "pedestrian"
        self.pos = pos
        self.destination = destination
        self.path = self.calculate_path()
        self.current_step = 0

        # Mensaje si la ruta no es válida
        if not self.path:
            print(f"Peatón {self.unique_id}: No se encontró una ruta válida de {self.pos} a {self.destination}.")    

    def calculate_path(self):
        """
        Calcula el camino desde la posición actual hasta el destino usando A*.
        :return: Una lista de posiciones representando el camino, o lista vacía si no hay ruta válida.
        """
        astar = Astar(self.model, self.pos, self.destination)
        return astar.find_path_ped()
    
    def recalculate_path(self):
        """
        Recalcula la ruta en tiempo real si hay bloqueos o cambios en el entorno.
        """
        new_path = Astar(self.model, self.pos, self.destination).find_path_ped()
        if new_path:
            self.path = new_path
            self.current_step = 0  # Reiniciar progreso en la nueva ruta
            print(f"Peatón {self.unique_id}: Ruta recalculada.")
        else:
            print(f"Peatón {self.unique_id}: No se pudo recalcular la ruta.")

    def detect_and_communicate_with_cars(self):
        """
        Detecta coches cercanos en una intersección y se comunica con ellos para detenerse.
        """
        # Obtener las posiciones alrededor del peatón (vecindad inmediata)
        x, y = self.pos
        neighboring_positions = [
            (x - 1, y), (x + 1, y),  # izquierda y derecha
            (x, y - 1), (x, y + 1)   # arriba y abajo
        ]

        for neighbor in neighboring_positions:
            if not self.model.grid.out_of_bounds(neighbor):  # Verificar si la posición está dentro de los límites
                cell_contents = self.model.grid.get_cell_list_contents(neighbor)
                for agent in cell_contents:
                    if getattr(agent, "type", None) == "car":  # Si el agente es un coche
                        print(f"Peatón {self.unique_id} detectó un coche en {neighbor}. Solicitando detenerse.")
                        agent.stop_for_pedestrian()  # Comunicar al coche que debe detenerse
        
    def is_valid_move(self, next_pos):
        """
        Verifica si la celda de destino es válida para el peatón.
        """
        # Verificar si la celda está dentro de las direcciones permitidas para peatones
        current_allowed_directions = self.model.direcciones_peatones.get(self.pos, [])
        if not current_allowed_directions:
            return False

        # Determinar la dirección del movimiento
        dx = next_pos[0] - self.pos[0]
        dy = next_pos[1] - self.pos[1]
        direction = None
        if dx == -1 and dy == 0:
            direction = 'left'
        elif dx == 1 and dy == 0:
            direction = 'right'
        elif dx == 0 and dy == -1:
            direction = 'up'
        elif dx == 0 and dy == 1:
            direction = 'down'

        if direction not in current_allowed_directions:
            return False

        # Verificar contenido de la celda de destino
        cell_contents = self.model.grid.get_cell_list_contents(next_pos)

        # Evitar celdas ocupadas por coches
        for agent in cell_contents:
            if agent.type == 'car':  # Si hay un coche en la celda
                return False

        return True


    def step(self):
        """
        Mueve al peatón a lo largo de su camino, recalcula la ruta si es necesario
        y detecta coches para comunicarse con ellos.
        """
        # Detectar y comunicarse con coches cercanos
        self.detect_and_communicate_with_cars()

        # Recalcular la ruta cada 10 pasos, por ejemplo
        if self.model.schedule.steps % 10 == 0:
            self.recalculate_path()

        if self.path and self.current_step < len(self.path):
            next_pos = self.path[self.current_step]

            # Verificar si la celda es válida
            if self.is_valid_move(next_pos):
                self.model.grid.move_agent(self, next_pos)
                self.current_step += 1
                print(f"Peatón {self.unique_id}: Se movió a {next_pos}.")
            else:
                print(f"Peatón {self.unique_id}: Celda no válida, recalculando ruta.")
                self.recalculate_path()
        elif self.current_step >= len(self.path) or self.pos == self.destination:
            print(f"Peatón {self.unique_id}: Llegó a su destino {self.destination} y será eliminado.")
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)



