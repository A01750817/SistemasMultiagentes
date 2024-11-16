import mesa
from car_agent import CarAgent
from traffic_light import Traffic_light

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=24, height=24):
        super().__init__()
        self.num_agents = numberAgents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.traffic_lights = []
        self.garajes = [(4,4), (4, 11), (2, 8), (8, 9), (9, 2), (10, 11), (11, 6), (17, 2), (20, 5), (20, 8), 
           (18, 11), (3, 17), (10, 16), (4, 20), (8, 21), (17, 17), (21, 20)]
        initial_positions = [(18, 11)]
        # Define restricted cells (buildings, garages, etc.)
        self.celdas_restringidas = [
            (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4), (5, 2), (5, 3), (5, 4),
            (2, 7), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8), (5, 8), (2, 9), (3, 9), (4, 9), (5, 9),
            (2, 10), (3, 10), (4, 10), (5, 10), (2, 11), (3, 11), (5, 11),
            (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 10), (8, 11), (9, 3), (9, 4),
            (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (10, 2), (10, 3), (10, 4), (10, 5),
            (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (11, 2), (11, 3), (11, 4), (11, 5), (11, 7),
            (11, 8), (11, 9), (11, 10), (11, 11), (16, 2), (16, 3), (16, 4), (16, 5), (17, 3), (17, 4),
            (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (21, 5), (16, 8), (16, 9),
            (16, 10), (16, 11), (17, 8), (17, 9), (17, 10), (17, 11), (18, 8), (18, 9), (18, 10), (19, 8),
            (19, 9), (19, 10), (19, 11), (20, 9), (20, 10), (20, 11), (21, 8), (21, 9), (21, 10), (21, 11),
            (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (11, 16), (2, 17),
            (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (2, 20), (3, 20),
            (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (11, 20), (10, 20), (2, 21), (3, 21), (4, 21),
            (5, 21), (6, 21), (7, 21), (9, 21), (10, 21), (11, 21), (16, 16), (16, 17), (17, 16),
            (16, 20), (16, 21), (17, 20), (17, 21), (20, 16), (20, 17), (21, 16), (21, 17), (20, 20),
            (20, 21), (21, 21), (13, 13), (14, 13), (14, 14), (13, 14),
        ]

        # Define directions
        direcciones_izquierda = [
            [(x, y) for x in range(25) for y in range(0,2)],
            [(x, y) for x in range(2,8) for y in range(5,7)],
            [(x, y) for x in range(2,14) for y in range(12,14)],
            [(x, y) for x in range(16,24) for y in range(12,14)],
            [(x, y) for x in range(16,24) for y in range(18,20)],
            [(2, 8), (8, 9), (12, 6), (18, 2), (20, 5), (18, 17), (22, 20)]
        ]

        direcciones_derecha = [
            [(x, y) for x in range(0,12) for y in range(14,16)],
            [(x, y) for x in range(0,12) for y in range(18,20)],
            [(x, y) for x in range(14,22) for y in range(14,16)],
            [(x, y) for x in range(14,22) for y in range(6,8)],
            [(x, y) for x in range(-1, 24) for y in range(22,24)],
            [(1, 8), (7, 9), (11, 6), (17, 2), (19, 5), (17, 17), (21, 20)]
        ]

        direcciones_abajo = [
            [(x, y) for x in range(2) for y in range(-1, 24)],
            [(x, y) for x in range(6, 8) for y in range(0, 12)],
            [(x, y) for x in range(12, 14) for y in range(0, 12)],
            [(x, y) for x in range(12, 14) for y in range(14, 22)],
            [(x, y) for x in range(18, 20) for y in range(14, 22)],
            [(9, 1), (4, 19), (8, 21), (3, 17), (4, 4), (4, 11), (10, 11), 
             (18, 11), (20, 7), (10, 15), (17, 1), (20, 5), (17, 17), (21, 19)]
        ]

        direcciones_arriba = [
            [(x, y) for x in range(22, 24) for y in range(0, 25)],
            [(x, y) for x in range(14, 16) for y in range(2, 14)],
            [(x, y) for x in range(14, 16) for y in range(16, 24)],
            [(x, y) for x in range(18, 20) for y in range(2, 8)],
            [(9, 2), (4, 20), (8, 22), (3, 18), (4, 5), (4, 12), (10, 12), 
             (18, 12), (20, 8), (10, 16), (17, 2), (20, 6), (17, 18), (21, 20)]
        ]

        # Create allowed directions dictionary
        self.direcciones_permitidas = {}
        self._populate_allowed_directions(direcciones_izquierda, 'left')
        self._populate_allowed_directions(direcciones_derecha, 'right')
        self._populate_allowed_directions(direcciones_abajo, 'down')
        self._populate_allowed_directions(direcciones_arriba, 'up')

        self.initial_positions = initial_positions or [None] * self.num_agents

        # Create traffic lights and agents
        self.create_traffic_lights()
        self.create_agents()

        
    def _populate_allowed_directions(self, direction_lists, direction):
        for sublist in direction_lists:
            for pos in sublist:
                if pos not in self.direcciones_permitidas:
                    self.direcciones_permitidas[pos] = []
                self.direcciones_permitidas[pos].append(direction)

    def create_traffic_lights(self):
        traffic_light_positions = [
            (0, 4), (1, 4), (2, 5), (2, 6), (11, 18), (11, 19), (12, 17), (13, 17),
            (18, 2), (19, 2), (18, 17), (19, 17), (20, 0), (20, 1), (20, 18),
            (20, 19), (21, 6), (21, 7), (22, 8), (23, 8)
        ]
        for i, pos in enumerate(traffic_light_positions):
            if pos not in self.celdas_restringidas and self.grid.is_cell_empty(pos):
                semaforo = Traffic_light(self, 100 + i + 1, pos, timer_interval=10)
                self.grid.place_agent(semaforo, pos)
                self.schedule.add(semaforo)
                self.traffic_lights.append(semaforo)

    def create_agents(self):
        for i in range(self.num_agents):
            # Usar la posición inicial proporcionada o asignar aleatoriamente
            if self.initial_positions[i] is not None:
                pos = self.initial_positions[i]
            else:
                while True:
                    pos = (self.random.randrange(self.width), self.random.randrange(self.height))
                    if pos not in self.celdas_restringidas and self.grid.is_cell_empty(pos):
                        break

            # Asignar un destino aleatorio de los garajes
            destination = (9, 2)

            # Crear el agente de carro con su destino
            traffic_light_ref = self.traffic_lights[i % len(self.traffic_lights)]
            car = CarAgent(self, i, pos, traffic_light_ref, destination)
            self.grid.place_agent(car, pos)
            self.schedule.add(car)


    def step(self):
        self.schedule.step()