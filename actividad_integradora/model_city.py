import mesa
from traffic_light import Traffic_light
from car_agent import CarAgent

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=24, height=24):
        super().__init__()
        self.num_agents = numberAgents
        # Cambiar a MultiGrid para permitir múltiples agentes en la misma celda
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.width = width
        self.height = height
        self.create_agents()
        self.create_traffic_lights()

    def create_agents(self):
        for i in range(self.num_agents):
            # Generar una posición aleatoria para el coche
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            car = CarAgent(self, i, pos)  # Pasar model, unique_id, pos
            self.grid.place_agent(car, pos)
            self.schedule.add(car)

    def create_traffic_lights(self):
        # Crear semáforos en las coordenadas (0, 4) y (1, 4)
        semaforo1 = Traffic_light(100 + 1, self, (0, 4), timer_interval=5)
        semaforo2 = Traffic_light(100 + 2, self, (1, 4), timer_interval=5)
        
        # Agregar los semáforos al grid y al schedule
        self.grid.place_agent(semaforo1, (0, 4))
        self.grid.place_agent(semaforo2, (1, 4))
        self.schedule.add(semaforo1)
        self.schedule.add(semaforo2)

    def step(self):
        self.schedule.step()