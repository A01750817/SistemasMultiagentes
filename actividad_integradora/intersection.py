# intersection.py

# intersection.py

import mesa
from car_agent import CarAgent

class Intersection(mesa.Agent):
    def __init__(self, unique_id, model, traffic_lights, timer_interval=10):
        super().__init__(unique_id, model)
        self.traffic_lights = traffic_lights  # Lista de Traffic_light
        self.timer_interval = timer_interval
        self.timer = 0
        self.state = True  # True: NS verde, EW rojo; False: NS rojo, EW verde
        self.initial_delay = 5  # Retraso inicial en pasos

        # Inicializar estados de los semáforos a rojo
        for light in self.traffic_lights:
            light.state = False  # Todas las luces en rojo

    def step(self):
        # Implementación del retraso inicial
        if self.initial_delay > 0:
            # Mantener todas las luces en rojo
            for light in self.traffic_lights:
                light.state = False
            self.initial_delay -= 1
            print(f"Intersección {self.unique_id} en retraso inicial, todas las luces en rojo. Tiempo restante: {self.initial_delay}")
            return

        # Lógica existente
        # Detectar carros en cada dirección
        cars_in_ns = self.detect_cars_in_direction('NS')
        cars_in_ew = self.detect_cars_in_direction('EW')
        print(f"Intersección {self.unique_id}: NS carros={cars_in_ns}, EW carros={cars_in_ew}")

        # Decidir el estado basado en la presencia de carros
        if cars_in_ns > cars_in_ew:
            desired_state = True  # Dar paso al tráfico NS
        elif cars_in_ew > cars_in_ns:
            desired_state = False  # Dar paso al tráfico EW
        else:
            # Si igual cantidad de carros, usar el temporizador para alternar
            self.timer += 1
            if self.timer >= self.timer_interval:
                desired_state = not self.state
                self.timer = 0
            else:
                desired_state = self.state

        # Actualizar estado si ha cambiado
        if desired_state != self.state:
            self.state = desired_state
            # Actualizar el estado de los semáforos
            for light in self.traffic_lights:
                if light.orientation == 'NS':
                    light.state = self.state
                elif light.orientation == 'EW':
                    light.state = not self.state
            print(f"Intersección {self.unique_id} cambia estado a {'NS verde, EW rojo' if self.state else 'NS rojo, EW verde'}")
        else:
            # Para depuración, mostrar el estado actual si no cambia
            print(f"Intersección {self.unique_id} mantiene estado {'NS verde, EW rojo' if self.state else 'NS rojo, EW verde'}")

        # Actualizar estado si ha cambiado
        if desired_state != self.state:
            self.state = desired_state
            # Actualizar el estado de los semáforos
            for light in self.traffic_lights:
                if light.orientation == 'NS':
                    light.state = self.state
                elif light.orientation == 'EW':
                    light.state = not self.state
            print(f"Intersección {self.unique_id} cambia estado a {'NS verde, EW rojo' if self.state else 'NS rojo, EW verde'}")
        else:
            # Para depuración, mostrar el estado actual si no cambia
            print(f"Intersección {self.unique_id} mantiene estado {'NS verde, EW rojo' if self.state else 'NS rojo, EW verde'}")

    def detect_cars_in_direction(self, direction):
        """
        Detecta el número de carros esperando en la dirección dada.
        
        - direction: 'NS' o 'EW'
        """
        count = 0
        for light in self.traffic_lights:
            if light.orientation == direction:
                # Obtener la posición delante del semáforo
                pos_ahead = (light.pos[0] + light.direction_vector[0],
                             light.pos[1] + light.direction_vector[1])
                # Verificar si la posición está dentro del grid
                if self.model.grid.out_of_bounds(pos_ahead):
                    continue
                # Obtener los agentes en la posición
                cell_contents = self.model.grid.get_cell_list_contents([pos_ahead])
                for agent in cell_contents:
                    if isinstance(agent, CarAgent):
                        count += 1
        return count
    
