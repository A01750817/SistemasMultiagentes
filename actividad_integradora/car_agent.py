import mesa

class CarAgent(mesa.Agent):
    """
    Clase que modela un carro como agente
    """
    def __init__(self, model, unique_id, pos, traffic_light):
        super().__init__(unique_id, model)
        self.pos = pos
        self.traffic_light = traffic_light

    def move(self):
        possible_movements = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )
        new_position = self.random.choice(possible_movements)
        self.model.grid.move_agent(self, new_position)

    def is_stop(self):
        if self.traffic_light.state:
            self.move()
            print("En movimiento")
        else:
            print("Detenido")

    def step(self):
        self.is_stop()



