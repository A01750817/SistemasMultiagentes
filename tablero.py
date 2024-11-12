# Importar las bibliotecas necesarias
import mesa
import numpy as np
import seaborn as sns

# Definicion del agente coche 
class CarAgent(mesa.Agent):
    def __init__(self, model, matricula):
        super().__init__(model, matricula)
        self.moves = 0
        
    def driveMove(self):
        #en coche puede moverse derecha, izquierda, arriba o abajo dependiendo de el centido de la calle
        # car can move right, left, up or down depending on the street direction
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False) #esto sirve para obtener los vecinos de la celda actual
        # this is to get the neighbors of the current cell
        next_step = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, next_step) #mueve el agente a la celda vecina
        
    
    def step(self):
        #si hay un estacionamiento al lado de la celda del agente, se estaciona
        # if current position has a parking lot in neighbor cells, park
        if self.model.grid.is_cell_empty(self.pos): #si la celda esta vacia
            self.model.grid.place_agent(self, self.pos) #coloca el agente en la celda
        else:
            #si no hay un estacionamiento al lado de la celda del agente, se mueve
            # if there is no parking lot in neighbor cells, move
            self.driveMove()

