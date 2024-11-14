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
        semaforo1 = Traffic_light(100 + 1, self, (1, 4), timer_interval=5)
        semaforo2 = Traffic_light(100 + 2, self, (2, 4), timer_interval=5)
        
        for agent in self.grid.get_cell_list_contents((1, 4)):
            self.grid.remove_agent(agent)
        self.grid.place_agent(semaforo1, (1, 4))

        for agent in self.grid.get_cell_list_contents((2, 4)):
            self.grid.remove_agent(agent)
        self.grid.place_agent(semaforo2, (2, 4))

        self.schedule.add(semaforo1)
        self.schedule.add(semaforo2)

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