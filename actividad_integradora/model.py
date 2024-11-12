import mesa
import matplotlib.pyplot as plt
import traffic_light 
import car_agent 

class cityClass(mesa.Model):
    def __init__(self, numberAgents=1, width=24, height=24):
        self.num_agents = numberAgents
        self.grid = mesa.space.SingleGrid(width, height) 
        self.car_schedule = mesa.time.RandomActivation(self)
        self.traffic_light_schedule = mesa.time.BaseScheduler(self)
        self.running = True
        self.width = width
        self.height = height
        self.create_agents()
        
        # agregar semaforos
        # add traffic lights que seran agents
        self.create_traffic_lights()
        
    def create_agents(self):
        for i in range(self.num_agents):
            car = car_agent.CarAgent(i, self)
            self.grid.place_agent(car, (self.random.randrange(self.width), self.random.randrange(self.height)))
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
        
# Ahora quiero visualizarlo con matploitlib
# Now I want to visualize it with matplotlib

