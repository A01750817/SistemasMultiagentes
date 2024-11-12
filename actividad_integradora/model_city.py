import mesa
import matplotlib.pyplot as plt
import traffic_light 
import car_agent 

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=24, height=24, torus=False):
        super().__init__()  # Inicializa la clase base mesa.Model
        self.num_agents = numberAgents
        self.grid = mesa.space.SingleGrid(width, height, torus) 
        self.car_schedule = mesa.time.RandomActivation(self)
        self.traffic_light_schedule = mesa.time.BaseScheduler(self)
        self.running = True
        self.width = width
        self.height = height
        self.create_agents()
        
        # Agregar semáforos
        self.create_traffic_lights()
        
    def create_agents(self):
        for i in range(self.num_agents):
            # Generar una posición aleatoria para el coche
            pos = (self.random.randrange(self.width), self.random.randrange(self.height))
            car = car_agent.CarAgent(self, i, pos)  # Pasar model, unique_id, pos
            self.grid.place_agent(car, pos)
            self.car_schedule.add(car)
        
    def create_traffic_lights(self):
        # Crear semáforos en las coordenadas (0, 4) y (1, 4)
        semaforo1 = traffic_light.Traffic_light(1, self, (0, 4), True)
        semaforo2 = traffic_light.Traffic_light(2, self, (1, 4), True)
        
        # Agregar los semáforos al grid y al schedule
        self.grid.place_agent(semaforo1, (0, 4))
        self.grid.place_agent(semaforo2, (1, 4))
        self.traffic_light_schedule.add(semaforo1)
        self.traffic_light_schedule.add(semaforo2)
        
    def step(self):
        self.car_schedule.step()
        self.traffic_light_schedule.step()