import mesa

class CarAgent(mesa.Agent):
    """
    Clase que modela un carro como agente
    """
    def __init__(self, model, unique_id, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def move(self):
        possible_movements = self.model.grid.get_neighborhood(
            self.pos,
            moore = False,
            include_center = False )
        new_position = self.random.choice(possible_movements)
        self.model.grid.move_agent(self, new_position)
    
    def is_stop(self):
        self.move()
        
    
    
    def step(self):
        self.is_stop()

class Traffic_light(mesa.Agent):
    def __init__(self, model, unique_id, pos, timer_interval=5):
        super().__init__(model, unique_id)
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
    def __init__(self, numberAgents=1, width=24, height=24):
        super().__init__()
        self.num_agents = numberAgents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.create_agents()
        self.create_traffic_lights()

    def create_agents(self):
        for i in range(self.num_agents):
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            car = CarAgent(self, i, pos)
            # Elimina agentes de la posición si ya existen
            for agent in self.grid.get_cell_list_contents(pos):
                self.grid.remove_agent(agent)
            self.grid.place_agent(car, pos)
            self.schedule.add(car)

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

    def step(self):
        self.schedule.step()
