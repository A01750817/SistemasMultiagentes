# Actividad Integradora
# Codigo que modela el agente de los semaforos
# Autores:
# Santiago Villazón Ponce de León	A01746396
# Juan Antonio Figueroa Rodríguez	A01369043
# Iván Alexander Ramos Ramírez		A01750817
# Sebastián Antonio Almanza			A01749694
# Fecha de creación: 12/11/2024
# Última modificación: 15/11/2024
# Fecha de entrega 15/11/2024

import asyncio
import websockets
# traffic_light.py

import mesa

class Traffic_light(mesa.Agent):
    def __init__(self, unique_id, model, pos, orientation):
        """
        Inicializa un semáforo con posición y orientación.
        
        - unique_id: Identificador único del semáforo.
        - model: Referencia al modelo.
        - pos: Posición del semáforo en el grid.
        - orientation: 'NS' o 'EW'.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.orientation = orientation  # 'NS' o 'EW'
        self.state = False  # Inicialmente en rojo; será configurado por la intersección
        self.intersection = None  # Será asignado después
        self.type = "traffic_light"  # Agregado para evitar AttributeError

        # Definir el vector de dirección para detectar carros
        if self.orientation == 'NS':
            self.direction_vector = (0, 1)  # Hacia el sur
        elif self.orientation == 'EW':
            self.direction_vector = (1, 0)  # Hacia el este

    def step(self):
        """
        La lógica del semáforo es manejada por la intersección, por lo que este método no hace nada.
        """
        pass
