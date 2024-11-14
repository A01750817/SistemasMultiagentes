import mesa

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
