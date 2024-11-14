import mesa
from traffic_light import Traffic_light
from car_agent import CarAgent

class cityClass(mesa.Model):
    def __init__(self, numberAgents=20, width=24, height=24):
        super().__init__()
        self.num_agents = numberAgents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.traffic_lights = []  # To store traffic light objects
        self.create_traffic_lights()
        self.create_agents()

    def create_traffic_lights(self):
        traffic_light_positions = [(0, 4), (1, 4), (2, 5), (2, 6), (11, 18), (11, 19), (12, 17), (13, 17), (18, 2), 
                                   (19, 2), (18, 17), (19, 17), (20, 0), (20, 1), (20, 18), (20, 19), (21, 6), (21, 7), (22, 8), (23, 8)]
        for i, pos in enumerate(traffic_light_positions):
            if pos[0] < self.width and pos[1] < self.height:
                for agent in self.grid.get_cell_list_contents(pos):
                    self.grid.remove_agent(agent)
                semaforo = Traffic_light(self, 100 + i + 1, pos, timer_interval = 10)
                self.grid.place_agent(semaforo, pos)
                self.schedule.add(semaforo)
                self.traffic_lights.append(semaforo)

    def create_agents(self):
        for i in range(self.num_agents):
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            for agent in self.grid.get_cell_list_contents(pos):
                self.grid.remove_agent(agent)
            traffic_light_ref = self.traffic_lights[i % len(self.traffic_lights)]  # Assign traffic light
            car = CarAgent(self, i, pos, traffic_light_ref)
            self.grid.place_agent(car, pos)
            self.schedule.add(car)

    def step(self):
        self.schedule.step()