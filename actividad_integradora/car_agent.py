import mesa
import traffic_light

class CarAgent(mesa.Agent):
    """
    Clase que modela un carro como agente
    """
    def __init__(self, model, unique_id, pos):
        super().__init_(model)

    def move(self):
        possible_movements = self.model.grid.get_neighborhood(
            self.pos,
            moore = False,
            include_center = False )
        new_position = self.random.choice(possible_movements)
        self.model.grid.move_agent(self, new_position)
    
    def is_stop(self):
        if(traffic_light.state == True):
            self.move()
            print("En movimiento")
        elif(traffic_light.state == False):
            print("Detenido")
        else: 
            self.move()
        
    
    
    def step(self):
        self.is_stop()


