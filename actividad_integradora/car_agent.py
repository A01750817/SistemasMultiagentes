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
    # Obtener las posiciones posibles para moverse, excluyendo edificios
        possible_movements = [pos for pos in self.model.grid.get_neighborhood(
        self.pos,
        moore=False,
        include_center=False
    ) if pos not in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4), (5, 2), (5, 3), (5, 4),
    (2, 7), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8), (5, 8), (2, 9), (3, 9), (4, 9), (5, 9), 
    (2, 10), (3, 10), (4, 10), (5, 10), (2, 11), (3, 11), (5, 11),
    (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 10), (8, 11), (9, 3), (9, 4), 
    (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (10, 2), (10, 3), (10, 4), (10, 5), 
    (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (11, 2), (11, 3), (11, 4), (11, 5), (11, 7), 
    (11, 8), (11, 9), (11, 10), (11, 11), (16, 2), (16, 3), (16, 4), (16, 5), (17, 3), (17, 4), 
    (17, 5), (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (21, 5), (16, 8), (16, 9), 
    (16, 10), (16, 11), (17, 8), (17, 9), (17, 10), (17, 11), (18, 8), (18, 9), (18, 10), (19, 8), 
    (19, 9), (19, 10), (19, 11), (20, 9), (20, 10), (20, 11), (21, 8), (21, 9), (21, 10), (21, 11), 
    (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (11, 16), (2, 17), 
    (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (2, 20), (3, 20), 
    (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (11, 20), (10, 20), (2, 21), (3, 21), (4, 21), 
    (5, 21), (6, 21), (7, 21), (9, 21), (10, 21), (11, 21), (16, 16), (16, 17), (17, 16), 
    (16, 20), (16, 21), (17, 20), (17, 21), (20, 16), (20, 17), (21, 16), (21, 17), (20, 20), 
    (20, 21), (21, 21), (13, 13), (14, 13), (14, 14), (13, 14),]]

    # Mover solo si hay una posición disponible
        if possible_movements:
            new_position = self.random.choice(possible_movements)
            self.model.grid.move_agent(self, new_position)

    def is_stop(self):
        # Solo moverse si el semáforo está en verde o si el coche no está en la posición del semáforo
        if self.traffic_light.state or self.pos != self.traffic_light.pos:
            self.move()
            print("En movimiento")
        else:
            print("Detenido")

    def step(self):
        self.is_stop()
