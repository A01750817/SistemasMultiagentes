# Actividad Integradora
# Codigo que modela el agente de los semaforos
# Autores:
# Santiago Villazón Ponce de León   A01746396
# Juan Antonio Figueroa Rodríguez   A01369043
# Iván Alexander Ramos Ramírez      A01750817
# Sebastián Antonio Almanza         A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024

import mesa
import asyncio
import websockets

class Traffic_light(mesa.Agent):
    """
    Clase que modela un agente semáforo dentro de la simulación de la ciudad.
    ## Atributos:
    - model (cityClass): Referencia al modelo al que pertenece el semáforo.
    - unique_id (int): Identificador único del semáforo.
    - pos (tuple): Posición del semáforo en la cuadrícula (x, y).
    - state (bool): Estado actual del semáforo (`False` para rojo, `True` para verde).
    - timer (int): Contador interno que rastrea el tiempo transcurrido desde el último cambio de estado.
    - timer_interval (int): Intervalo de tiempo (en pasos de simulación) entre cambios de estado.
    ## Métodos:
    - __init__(self, model, unique_id, pos, timer_interval=10): Inicializa un semáforo con una posición, un estado inicial (rojo) y un intervalo de tiempo para alternar su estado.
    - step(self): Realiza un paso en la simulación. Incrementa el temporizador y alterna el estado del semáforo si el temporizador
    alcanza el intervalo configurado.
    """
    def __init__(self, model, unique_id, pos, timer_interval=10):
        """
        Inicializa un semaforo con una posicion, un estado inicial (rojo) y un intervalo de tiempo para alternar su estado.
        ## Argumentos:
        - model (cityClass): Referencia al modelo al que pertenece el semaforo.
        - unique_id (int): Identificador único del semaforo.
        - pos (tuple): Posición del semaforo en la cuadrícula (x, y).
        - timer_interval (int): Intervalo de tiempo (en pasos de simulación) entre cambios de estado.
        - self.type crea el agente "traffic_light" como agente, util para identificarlo dentro del modelo.
        - intersection_group agrupa los semáforos que pertenecen a la misma intersección o cuadrante.
        - self.count almacena la cantidad de coches que detecta el semáforo en frente de su posición.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.timer_interval = timer_interval
        self.state = False  # False = rojo, True = verde
        self.timer = 0
        self.type = "traffic_light"
        self.intersection_group = None  # Grupo de semáforos en la misma intersección
        self.cars_count = 0

    def count_cars(self):
        """
        Cuenta el número de coches en espera frente al semáforo.
        """
        self.cars_count = 0
        direction_offsets = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        for offset in direction_offsets.values():
            pos_to_check = (self.pos[0] + offset[0], self.pos[1] + offset[1])
            if not self.model.grid.out_of_bounds(pos_to_check):
                cell_contents = self.model.grid.get_cell_list_contents(pos_to_check)
                self.cars_count += sum(1 for agent in cell_contents if getattr(agent, "type", None) == "car")

                if self.cars_count > 0:
                    print(f"La cantidad de coches frente al semaforo son {self.pos}: {self.cars_count} coches")

    def __count_cars(self, offset):
        """
        Cuenta los coches en una dirección específica.
        """
        cell = self.pos
        count = 0
        for _ in range(4):  # Verifica hasta 4 celdas de distancia
            cell = (cell[0] + offset[0], cell[1] + offset[1])
            if self.model.grid.out_of_bounds(cell):
                break
            contents = self.model.grid.get_cell_list_contents(cell)
            for agent in contents:
                if getattr(agent, "type", None) == "car":
                    count += 1
        self.cars_count += count

    def __get_cars_in_line(self, direction):
        """
        Determina en qué dirección contar coches.
        """
        if direction == 'right':
            self.__count_cars((-1, 0))
        elif direction == 'left':
            self.__count_cars((1, 0))
        elif direction == 'up':
            self.__count_cars((0, -1))
        elif direction == 'down':
            self.__count_cars((0, 1))

    def synchronize_with_intersection(self):
        """
        Sincroniza el estado de los semáforos dentro de la misma intersección.
        Alterna estados entre pares norte-sur y este-oeste.
        """
        if not self.intersection_group:
            return  # Si no tiene grupo, no puede sincronizarse

        # Verificar si es tiempo de cambiar de estado
        if self.timer >= self.timer_interval:
            # Invertir estados para el grupo completo
            for light in self.intersection_group:
                light.state = not light.state
                light.timer = 0  # Reiniciar el temporizador
        else:
            self.timer += 1  # Incrementar el temporizador

    def prioritize_pair_in_quadrant(self):
        """
        Verifica en su cuadrante cuál par de semáforos tiene más coches.
        Cambia el estado del par con más coches, si aplica.
        """
        if not self.intersection_group:
            return  # Si no hay grupo, no se realiza la priorización

        # Separar los semáforos en norte-sur y este-oeste
        ns_lights = [light for light in self.intersection_group if light.state]
        ew_lights = [light for light in self.intersection_group if not light.state]

        # Contar coches en cada grupo
        ns_cars = sum(light.cars_count for light in ns_lights)
        ew_cars = sum(light.cars_count for light in ew_lights)

        # Si el grupo en rojo tiene más coches, cambiar estados
        if ew_cars > ns_cars:
            for light in ew_lights:
                light.state = True  # Verde
                light.timer = 0
            for light in ns_lights:
                light.state = False  # Rojo
                light.timer = 0
        elif ns_cars > ew_cars:
            for light in ns_lights:
                light.state = True  # Verde
                light.timer = 0
            for light in ew_lights:
                light.state = False  # Rojo
                light.timer = 0

    def step3(self):
        """
        Tercer paso en el ciclo de programación.
        Realiza acciones específicas dependiendo de la dirección.
        """
        if self.model.num_steps % 11 != 0 and self.model.num_steps != 1:
            pass
        else:
            direction = self.__get_light_direction()
            self.__get_cars_in_line(direction)
            self.__add_pairs()

    def step(self):
        """
        Actualiza el estado del semáforo en cada paso de la simulación.
        """
        self.count_cars()
        self.prioritize_pair_in_quadrant()
        self.synchronize_with_intersection()

