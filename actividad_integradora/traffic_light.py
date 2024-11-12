import mesa

class Traffic_light(mesa.Agent):
    def __init__(self, model, unique_id, pos):
        super().__init__(model)
        