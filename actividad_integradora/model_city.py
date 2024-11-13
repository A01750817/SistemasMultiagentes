import mesa
from traffic_light import Traffic_light
from car_agent import CarAgent

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=24, height=24, torus=False):
        super().__init__()
        self.num_agents = numberAgents
        # Cambiar a MultiGrid para permitir múltiples agentes en la misma celda
        self.grid = mesa.space.MultiGrid(width, height, torus)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.create_agents()
        self.create_traffic_lights()

    def create_agents(self):
        for i in range(self.num_agents):
            car = CarAgent(i, self)
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            self.grid.place_agent(car, pos)
            self.schedule.add(car)

    def create_traffic_lights(self):
        semaforo1 = Traffic_light(100 + 1, self, (0, 4), timer_interval=5)
        semaforo2 = Traffic_light(100 + 2, self, (1, 4), timer_interval=5)
        self.grid.place_agent(semaforo1, (0, 4))
        self.grid.place_agent(semaforo2, (1, 4))
        self.schedule.add(semaforo1)
        self.schedule.add(semaforo2)

    def step(self):
        self.schedule.step()
