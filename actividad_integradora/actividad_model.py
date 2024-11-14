import mesa

class CarAgent(mesa.Agent):
    def __init__(self, model, unique_id, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def move(self):
        possible_movements = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )
        new_position = self.random.choice(possible_movements)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

class Traffic_light(mesa.Agent):
    def __init__(self, model, unique_id, pos, timer_interval=5):
        super().__init__(unique_id, model)
        self.state = False
        self.pos = pos
        self.timer = 0
        self.timer_interval = timer_interval

    def step(self):
        self.timer += 1
        if self.timer >= self.timer_interval:
            self.state = not self.state
            self.timer = 0

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=25, height=25):
        super().__init__()
        self.num_agents = numberAgents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.create_agents()
        self.create_traffic_lights()

    def create_agents(self):
        for i in range(self.num_agents):
            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))
            # Limpia agentes en la posición actual si ya existen
            for agent in self.grid.get_cell_list_contents(pos):
                self.grid.remove_agent(agent)
            car = CarAgent(self, i, pos)
            self.grid.place_agent(car, pos)
            self.schedule.add(car)

    def create_traffic_lights(self):
        for i, pos in enumerate([(0, 5), (1, 5), (2,6), (2,7), (12, 19), (12, 20), (13, 18), (14, 18), (19, 3), (20, 3), (21, 1), (21, 2), (22, 7), (22, 8), (23, 9), (24, 9), (19, 18), (20, 18), (21, 19), (21, 20)], start=1):
            # Limpia agentes en la posición actual si ya existen
            for agent in self.grid.get_cell_list_contents(pos):
                self.grid.remove_agent(agent)
            semaforo = Traffic_light(self, 100 + i, pos, timer_interval=5)
            self.grid.place_agent(semaforo, pos)
            self.schedule.add(semaforo)

    def step(self):
        self.schedule.step()

