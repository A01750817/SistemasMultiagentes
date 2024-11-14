import mesa
from traffic_light import Traffic_light
from car_agent import CarAgent

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=20, height=20):
        super().__init__()
        self.num_agents = numberAgents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.create_traffic_lights()
        self.create_agents()

    def create_traffic_lights(self):
        traffic_light_positions = [(1, 4), (2, 4)]
        for i, pos in enumerate(traffic_light_positions):
            if pos[0] < self.width and pos[1] < self.height:
                for agent in self.grid.get_cell_list_contents(pos):
                    self.grid.remove_agent(agent)
                semaforo = Traffic_light(100 + i + 1, self, pos, timer_interval=5)
                self.grid.place_agent(semaforo, pos)
                self.schedule.add(semaforo)

    def create_agents(self):
        for i in range(self.num_agents):
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            for agent in self.grid.get_cell_list_contents(pos):
                self.grid.remove_agent(agent)
            car = CarAgent(self, i, pos)
            self.grid.place_agent(car, pos)
            self.schedule.add(car)

    def step(self):
        self.schedule.step()