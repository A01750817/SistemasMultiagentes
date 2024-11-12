import mesa

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
    
    def step(self):
        self.move()


