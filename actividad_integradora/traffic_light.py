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
import mesa

class Traffic_light(mesa.Agent):
    """
    Clase que modela un agente semáforo dentro de la simulación de la ciudad.
    ## Atributos:
    - model (cityClass): Referencia al modelo al que pertenece el semáforo.
    - unique_id (int): Identificador único del semáforo.
    - pos (tuple): Posición del semáforo en la cuadrícula (x, y).
    - state (bool): Estado actual del semáforo (`False` para rojo, `True` para verde).
    - timer (int): Contador interno que rastrea el tiempo transcurrido desde el último cambio de estado.
    - timer_interval (int): Intervalo de tiempo (en pasos de simulación) entre cambios de estado.
    ## Métodos:
    - __init__(self, model, unique_id, pos, timer_interval=10): Inicializa un semáforo con una posición, un estado inicial (rojo) y un intervalo de tiempo para alternar su estado.
    - step(self): Realiza un paso en la simulación. Incrementa el temporizador y alterna el estado del semáforo si el temporizador
    alcanza el intervalo configurado.
    """
    def __init__(self, model, unique_id, pos, timer_interval):
        """
        Inicializa un semaforo con una posicion, un estado inicial (rojo) y un intervalo de tiempo para alternar su estado.
        ## Argumentos:
        - model (cityClass): Referencia al modelo al que pertenece el semaforo.
        - unique_id (int): Identificador único del semaforo.
        - pos (tuple): Posición del semaforo en la cuadrícula (x, y).
        - timer_interval (int): Intervalo de tiempo (en pasos de simulación) entre cambios de estado.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.timer_interval = timer_interval
        self.state = True  # True = verde, False = rojo
        self.timer = 0
        self.type = "traffic_light"  # Para identificarlo como semáforo

    def step(self):
        """
        Función que realiza un paso en la simulación. Incrementa el temporizador y alterna el estado del semáforo si el temporizador alcanza el intervalo configurado.
        """
        self.timer += 1
        if self.timer >= self.timer_interval:
            self.state = not self.state  # Cambia entre True y False
            self.timer = 0  # Reinicia el temporizador
