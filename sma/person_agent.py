import mesa
from astar import Astar
import random

class PersonAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos, destination):
        super().__init__(unique_id, model)
        self.type = "pedestrian"
        self.pos = pos
        self.destination = destination
        self.original_destination = destination  # Guardar el destino original
        self.path = self.calculate_path()
        self.current_step = 0
        self.on_bus = False       # Indica si el peatón está en un bus
        self.bus = None           # Referencia al autobús si está a bordo
        self.waiting_at_bus_stop = False  # Indica si el peatón está esperando en una parada de bus
        self.waiting_counter = 0          # Contador de espera en la parada de bus
        self.max_waiting_time = 10        # Tiempo máximo de espera en la parada (en pasos de simulación)

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
        """Recalcula la ruta si hay cambios en el entorno."""
        if self.pos is None or self.destination is None:
            return  # No recalcular si la posición o el destino son None

        new_path = Astar(self.model, self.pos, self.destination).find_path_ped()
        if new_path:
            self.path = new_path
            self.current_step = 0
            print(f"Peatón {self.unique_id}: Ruta recalculada.")
        else:
            print(f"Peatón {self.unique_id}: No se pudo recalcular la ruta.")
            self.destination = None
        
    def detect_and_communicate_with_cars(self):
        """
        Detecta coches cercanos en una intersección y se comunica con ellos para detenerse.
        """
        # Obtener las posiciones alrededor del peatón (vecindad inmediata)
        x, y = self.pos
        neighboring_positions = [
            (x - 2, y), (x + 2, y),  # izquierda y derecha
            (x, y - 2), (x, y + 2)   # arriba y abajo
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
    
    
    def is_adjacent_to_bus_stop(self):
        """
        Verifica si hay una parada de bus en las celdas adyacentes a la posición actual del peatón
        en las direcciones arriba, abajo, izquierda y derecha.
        """
        x, y = self.pos
        adjacent_positions = [
            (x - 1, y),  # Izquierda
            (x + 1, y),  # Derecha
            (x, y - 1),  # Arriba
            (x, y + 1)   # Abajo
        ]
        for pos in adjacent_positions:
            if pos in self.model.bus_stops:
                return True
        return False
    
    def move_pedestrian(self):
        """
        Maneja el movimiento del peatón cuando no está esperando en una parada de bus.
        """
        # Detectar y comunicarse con coches cercanos
        self.detect_and_communicate_with_cars()

        if self.path and self.current_step < len(self.path):
            next_pos = self.path[self.current_step]

            # Verificar si hay un bus en la posición siguiente
            cell_contents = self.model.grid.get_cell_list_contents(next_pos)
            bus_found = False
            for agent in cell_contents:
                if getattr(agent, "type", None) == "bus" and agent.stop_counter > 0:
                    # Moverse sobre el bus y subirse
                    self.model.grid.move_agent(self, next_pos)
                    agent.passengers.append(self)
                    self.on_bus = True
                    self.bus = agent
                    self.model.grid.remove_agent(self)       # Quitar de la cuadrícula
                    self.model.schedule.remove(self)         # Quitar del scheduler
                    print(f"Peatón {self.unique_id}: Se subió al autobús {agent.unique_id}.")
                    return
            if not bus_found:
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
            self.pos = None  # Marcar la posición como None

    def step(self):
        """
        Mueve al peatón a lo largo de su camino, recalcula la ruta si es necesario,
        detecta coches para comunicarse con ellos, y gestiona el posible
        embarque en autobuses.
        """
        if self.on_bus or self.pos is None:
            # Si está en el bus o ha sido eliminado, no hace nada
            return

        # Verificar si ya está esperando en una parada de bus
        if self.waiting_at_bus_stop:
            self.waiting_counter += 1
            print(f"Peatón {self.unique_id}: Esperando en parada de bus ({self.waiting_counter}/{self.max_waiting_time}).")
            # Verificar si hay un bus en la parada
            cell_contents = self.model.grid.get_cell_list_contents(self.pos)
            for agent in cell_contents:
                if getattr(agent, "type", None) == "bus" and agent.stop_counter > 0:
                    # Subirse al bus
                    agent.passengers.append(self)
                    self.on_bus = True
                    self.bus = agent
                    self.model.grid.remove_agent(self)       # Quitar de la cuadrícula
                    self.model.schedule.remove(self)         # Quitar del scheduler
                    print(f"Peatón {self.unique_id}: Se subió al autobús {agent.unique_id}.")
                    return  # Salir del método step inmediatamente
            # Si el tiempo de espera excede el máximo, continuar caminando
            if self.waiting_counter >= self.max_waiting_time:
                self.waiting_at_bus_stop = False
                self.waiting_counter = 0
                print(f"Peatón {self.unique_id}: No llegó el bus, continúa su camino.")
        else:
            # Detectar si hay una parada de bus adyacente
            if self.is_adjacent_to_bus_stop():
                # Inicia el periodo de espera
                self.waiting_at_bus_stop = True
                self.waiting_counter = 0
                print(f"Peatón {self.unique_id}: Llegó a una parada de bus, comienza a esperar.")
                return  # Espera en la parada, no hace más acciones en este paso
            else:
                # Continuar con el movimiento normal
                self.move_pedestrian()

        # Recalcular la ruta cada 10 pasos, por ejemplo
        if self.model.schedule.steps % 10 == 0:
            self.recalculate_path()
            """
            Mueve al peatón a lo largo de su camino, recalcula la ruta si es necesario,
            detecta coches para comunicarse con ellos, y gestiona el posible
            embarque en autobuses.
            """
            if self.on_bus or self.pos is None:
                # Si está en el bus o ha sido eliminado, no hace nada
                return

            # Detectar y comunicarse con coches cercanos
            self.detect_and_communicate_with_cars()

            # Recalcular la ruta cada 10 pasos, por ejemplo
            if self.model.schedule.steps % 10 == 0:
                self.recalculate_path()

            # Verificar si está en una parada de bus
            if self.pos in self.model.bus_stops:
                # Verificar si hay un bus esperando en esta parada
                cell_contents = self.model.grid.get_cell_list_contents(self.pos)
                for agent in cell_contents:
                    if getattr(agent, "type", None) == "bus" and agent.stop_counter > 0:
                        # Hay un bus esperando, decidir si subirse
                        decision = True  # O implementa tu lógica de decisión
                        if decision:
                            # Subirse al bus
                            agent.passengers.append(self)
                            self.on_bus = True
                            self.bus = agent
                            self.model.grid.remove_agent(self)       # Quitar de la cuadrícula
                            self.model.schedule.remove(self)         # Quitar del scheduler
                            print(f"Peatón {self.unique_id}: Se subió al autobus {agent.unique_id}.")
                            return  # Salir del método step inmediatamente

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
                self.pos = None  # Opcional: marcar la posición como None