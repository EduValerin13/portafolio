'''
Equipo Sinko Peso
- Ricardo Hernández Rincón          | A00831818
- Eduardo Andrés Valerin Vijil      | A00830774
- Santiago Alejandro Minga Martínez | A00830698
- Julio Eduardo Arvizu Castillo     | A00831346
- Eunice Santos Galindo             | A00831991
- Brenda Elena Saucedo González     | A00829855
'''
# Model design
import agentpy as ap
import networkx as nx 
import random

# Visualization
import matplotlib.pyplot as plt 
import seaborn as sns
import IPython

# Data
import numpy as np
import json

class Car(ap.Agent):
    
  """ Initialize a new variable at agent creation. """
  def setup(self):
    self.condition = 0 # Conduciendo = 0, Standby = 1
    self.turn_chance = self.model.random
    self.grid = self.model.grid
    self.dir = 0 # Horizontal = 0, Vertical = 1
    self.side = 0 # Right = 0, Left = 1
    self.id = 0
        
        
        
  """ Manejar """
  def drive(self):
    if self.condition == 0:
      ### Setters iniciales
      if (self.grid.positions[self] == (0, int(self.p.gridsize/2))):
        self.dir = 1
      elif (self.grid.positions[self] == (self.p.gridsize, int(self.p.gridsize/2+1))):
        self.dir = 1
        self.side = 1
      elif (self.grid.positions[self] == (int(self.p.gridsize/2),self.p.gridsize)):
        self.side = 1

      ### Lado de la calle
      if self.side == 0: #Right      
        if self.condition == 0 and self.dir == 0:  #Horizontal
          self.grid.move_by(self, (0,1))
        elif self.condition == 0 and self.dir == 1: #Vertical
          self.grid.move_by(self, (1,0))
      else: #Left
        if self.condition == 0 and self.dir == 0:  #Horizontal
          self.grid.move_by(self, (0,-1))
        elif self.condition == 0 and self.dir == 1: #Vertical
          self.grid.move_by(self, (-1,0))
              
      ### Girar
      rng = self.model.random
      if ((self.grid.positions[self] == (int(self.p.gridsize/2),int(self.p.gridsize/2))
          and self.dir == 1 and self.side == 0)and  # street is Turnable (V-R)
        self.p.turn_chance > rng.random()):
        self.dir = 0
        self.side = 1
      elif ((self.grid.positions[self] == (int(self.p.gridsize/2),int(self.p.gridsize/2+1))
          and self.dir == 0 and self.side == 1) and  # street is Turnable (H-L)
        self.p.turn_chance > rng.random()):
        self.dir = 1
      elif ((self.grid.positions[self] == (int(self.p.gridsize/2+1),int(self.p.gridsize/2))
          and self.dir == 0 and self.side == 0) and  # street is Turnable (H-R)
        self.p.turn_chance > rng.random()):
        self.dir = 1
      elif ((self.grid.positions[self] == (int(self.p.gridsize/2+1),int(self.p.gridsize/2+1))
          and self.dir == 1 and self.side == 1)and  # street is Turnable (V-L)
        self.p.turn_chance > rng.random()):
        self.dir = 0
        self.side = 0



  """ Verifica que no hayan coches a su alrededor """
  def check_neighbor(self):

    # Posición del carro.
    car_pos = self.grid.positions[self]

    # Para evitar que los carros choquen.
    for neighbor in self.grid.neighbors(self):

      # Verifica que el agente sea un vehiculo.
      if neighbor.type == 'Car':

        # Vertical-Abajo
        if self.dir == 1 and self.side == 0:
          # Neighbor se dirija a la misma dirección.
          if neighbor.dir == 1 and neighbor.side == 0:
            if self.grid.positions[neighbor][0] == car_pos[0]+1 and self.grid.positions[neighbor][1] == car_pos[1]:
              self.condition = 1
              break
          # Neighbor se dirija H-D.
          elif neighbor.dir == 0 and neighbor.side == 0:
            # Caso neighbor se encuentre delante.
            if self.grid.positions[neighbor][0] == car_pos[0]+1 and self.grid.positions[neighbor][1] == car_pos[1]:
              self.condition = 1
              break
            # Caso neighbor este en contra esquina.
            elif self.grid.positions[neighbor][1]+1 == car_pos[1] and self.grid.positions[neighbor][0] == car_pos[0]+1:
              self.condition = 1
              break
          # Neighbor se dirija H-I.
          elif neighbor.dir == 0 and neighbor.side == 1:
            # Caso neighbor se encuentre delante.
            if self.grid.positions[neighbor][0] == car_pos[0]+1 and self.grid.positions[neighbor][1] == car_pos[1]:
              self.condition = 1
              break
            # Caso neighbor este en contra esquina.
            elif self.grid.positions[neighbor][1]-1 == car_pos[1] and self.grid.positions[neighbor][0] == car_pos[0]+1:
              self.condition = 1
              break

        # Vertical-Arriba
        if self.dir == 1 and self.side == 1:
          # Neighbor se dirija a la misma dirección.
          if neighbor.dir == 1 and neighbor.side == 1:
            if self.grid.positions[neighbor][0] == car_pos[0]-1 and self.grid.positions[neighbor][1] == car_pos[1]:
              self.condition = 1
              break
          # Neighbor se dirija H-D.
          elif neighbor.dir == 0 and neighbor.side == 0:
            # Caso neighbor se encuentre delante.
            if self.grid.positions[neighbor][0] == car_pos[0]-1 and self.grid.positions[neighbor][1] == car_pos[1]:
              self.condition = 1
              break
            # Caso neighbor este en contra esquina.
            elif self.grid.positions[neighbor][1]+1 == car_pos[1] and self.grid.positions[neighbor][0] == car_pos[0]-1:
              self.condition = 1
              break
          # Neighbor se dirija H-I.
          elif neighbor.dir == 0 and neighbor.side == 1:
            # Caso neighbor se encuentre delante.
            if self.grid.positions[neighbor][0] == car_pos[0]-1 and self.grid.positions[neighbor][1] == car_pos[1]:
              self.condition = 1
              break
            # Caso neighbor este en contra esquina.
            elif self.grid.positions[neighbor][1]-1 == car_pos[1] and self.grid.positions[neighbor][0] == car_pos[0]-1:
              self.condition = 1
              break

        # Horizontal-Derecha
        if (self.dir == 0 and self.side == 0) or neighbor.dir == 1:
          # Neighbor se dirija a la misma dirección.
          if neighbor.dir == 0 and neighbor.side == 0:
            if self.grid.positions[neighbor][1] == car_pos[1]+1 and self.grid.positions[neighbor][0] == car_pos[0]:
              self.condition = 1
              break

        # Horizontal-Izquierda
        if self.dir == 0 and self.side == 1:
          # Neighbor se dirija a la misma dirección.
          if (neighbor.dir == 0 and neighbor.side == 1) or neighbor.dir == 1:
            if self.grid.positions[neighbor][1] == car_pos[1]-1 and self.grid.positions[neighbor][0] == car_pos[0]:
              self.condition = 1
              break



class TLight(ap.Agent):

  """ Initialize a new variable at agent creation. """
  def setup(self):
    self.condition = 2 # Verde = 2, Rojo = 3
    self.grid = self.model.grid
    self.id = 0
    self.countRightLeft = 0
    self.countUpDown = 0
    self.is_Zero_RL = True
    self.is_Zero_UD = True
    self.minH = self.p.gridsize
    self.minV = self.p.gridsize
    self.dir = "horizontal"
    self.time_step_H = 0
    self.time_step_V = 0



  """ Realiza los calculos para analizar el tráfico. """
  def calculate(self):

    ### Parametros

    # Contadores para los carriles.
    self.countRightLeft = 0
    self.countUpDown = 0

    # Verfica que no este vacío uno de los contadores.
    self.is_Zero_RL = True
    self.is_Zero_UD = True

    # Obtiene la menor distancia desde la posición de un carro hasta al cruce del carril horizontal.
    self.minH = self.p.gridsize
    # Obtiene la menor distancia desde la posición de un carro hasta al cruce del carril vertical.
    self.minV = self.p.gridsize

    ### CALCULOS

    for car in self.model.agents:

      # HORIZONTAL & DERECHA/IZQUIERDA (verifica solo los que todavía no han pasado el cruce)
      if ((car.dir == 0 and car.side == 0 and self.grid.positions[car][1] >= 0 and
          self.grid.positions[car][1] <= int(self.p.gridsize/2-2)) or
          (car.dir == 0 and car.side == 1 and self.grid.positions[car][1] >= int(self.p.gridsize/2+3) and
          self.grid.positions[car][1] <= self.p.gridsize)):
        
        self.countRightLeft += 1
        
        self.is_Zero_RL = False

        aux = self.p.gridsize

        if (car.side == 0 and self.grid.positions[car][1] >= 0 and
            self.grid.positions[car][1] <= int(self.p.gridsize/2-2)):
          aux = int(self.p.gridsize/2) - 2 - self.grid.positions[car][1]
        elif (car.side == 1 and self.grid.positions[car][1] >= int(self.p.gridsize/2+3) and
            self.grid.positions[car][1] <= self.p.gridsize):
          aux = self.grid.positions[car][1] - int(self.p.gridsize/2) - 3

        if aux < self.minH:
          self.minH = aux

      # VERTICAL & ABAJO/ARRIBA (verifica solo los que todavía no han pasado el cruce)
      elif ((car.dir == 1 and car.side == 0 and self.grid.positions[car][0] >= 0 and
          self.grid.positions[car][0] <= int(self.p.gridsize/2-2)) or
          (car.dir == 1 and car.side == 1 and self.grid.positions[car][0] >= int(self.p.gridsize/2+3) and
          self.grid.positions[car][0] <= self.p.gridsize)):
        
        self.countUpDown += 1

        self.is_Zero_UD = False

        aux = self.p.gridsize

        if (car.side == 0 and self.grid.positions[car][0] >= 0 and
            self.grid.positions[car][0] <= int(self.p.gridsize/2-2)):
          aux = int(self.p.gridsize/2) - 2 - self.grid.positions[car][0]
        elif (car.side == 1 and self.grid.positions[car][0] >= int(self.p.gridsize/2+3) and
            self.grid.positions[car][0] <= self.p.gridsize):
          aux = self.grid.positions[car][0] - int(self.p.gridsize/2) - 3

        if aux < self.minV:
          self.minV = aux

        
  """ Verifica si cambiar de luz en base a los cálculos realizados. """
  def change_light(self):

    ### VERIFICACIONES PARA CAMBIAR DE COLOR LAS LUCES

    # Si es poco tráfico
    if self.countRightLeft < 10 and self.countUpDown < 10:

      # Verifica si en el carril horizontal hay un carro más cerca que el del vertical.
      if self.minH < self.minV:

        # Se verifica que el semáforo al menos este encendido por minimo "x" steps y como máximo "y" steps.
        if ( (self.time_step_V == 0 and self.time_step_H < self.p.max_time_light)
            or (self.time_step_V >= self.p.min_time_light) ):
          
          self.time_step_V = 0
          self.time_step_H += 1
            
          # Se cambia el estado de color del semáforo
          if self.dir == "vertical":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde

        else:

          self.time_step_H = 0
          self.time_step_V += 1

          # Se cambia el estado de color del semáforo
          if self.dir == "horizontal":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde


      # Verifica si en el carril vertical hay un carro más cerca que el del horizontal.
      elif self.minV < self.minH:

        # Se verifica que el semáforo al menos este encendido por minimo "x" steps y como máximo "y" steps.
        if ( (self.time_step_H == 0 and self.time_step_V < self.p.max_time_light)
            or (self.time_step_H >= self.p.min_time_light) ):
          
          self.time_step_H = 0
          self.time_step_V += 1

          # Se cambia el estado de color del semaforo
          if self.dir == "horizontal":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde
        
        else:

          self.time_step_V = 0
          self.time_step_H += 1

          # Se cambia el estado de color del semaforo
          if self.dir == "vertical":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde


      # Verifica si en el carril horizontal hay menos tráfico
      elif (not self.is_Zero_RL and self.countRightLeft < self.countUpDown) or self.is_Zero_UD:

        # Se verifica que el semáforo al menos este encendido por minimo "x" steps y como máximo "y" steps.
        if ( (self.time_step_V == 0 and self.time_step_H < self.p.max_time_light)
            or (self.time_step_V >= self.p.min_time_light) ):
          
          self.time_step_V = 0
          self.time_step_H += 1
            
          # Se cambia el estado de color del semáforo.
          if self.dir == "vertical":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde

        else:

          self.time_step_H = 0
          self.time_step_V += 1

          # Se cambia el estado de color del semáforo
          if self.dir == "horizontal":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde


      # Verifica si en el carril vertical hay menos tráfico.
      elif (not self.is_Zero_UD and self.countUpDown < self.countRightLeft) or self.is_Zero_RL:

        # Se verifica que el semáforo al menos este encendido por minimo "x" steps y como máximo "y" steps.
        if ( (self.time_step_H == 0 and self.time_step_V < self.p.max_time_light)
            or (self.time_step_H >= self.p.min_time_light) ):
          
          self.time_step_H = 0
          self.time_step_V += 1

          # Se cambia el estado de color del semáforo.
          if self.dir == "horizontal":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde
        
        else:

          self.time_step_V = 0
          self.time_step_H += 1

          # Se cambia el estado de color del semáforo.
          if self.dir == "vertical":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde


      # En caso de que no entre a ninguna condición, se queda con los mismos semáforos que estaban en verde y rojo.
      else:
        if (self.dir == "horizontal" and self.condition == 2) or (self.dir == "vertical" and self.condition == 3):
          self.time_step_V = 0
          self.time_step_H += 1
        elif (self.dir == "vertical" and self.condition == 2) or (self.dir == "horizontal" and self.condition == 3):
          self.time_step_H = 0
          self.time_step_V += 1


    # Si es mucho tráfico.
    else:

      # Verifica si en el carril horizontal hay menos tráfico.
      if (not self.is_Zero_RL and self.countRightLeft > self.countUpDown) or self.is_Zero_UD:

        # Se verifica que el semáforo al menos este encendido por minimo "x" steps y como máximo "y" steps.
        if ( (self.time_step_V == 0 and self.time_step_H < self.p.max_time_light)
            or (self.time_step_V >= self.p.min_time_light) ):
          
          self.time_step_V = 0
          self.time_step_H += 1
            
          # Se cambia el estado de color del semáforo.
          if self.dir == "vertical":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde

        else:

          self.time_step_H = 0
          self.time_step_V += 1

          # Se cambia el estado de color del semáforo.
          if self.dir == "horizontal":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde


      # Verifica si en el carril vertical hay menos tráfico
      elif (not self.is_Zero_UD and self.countUpDown > self.countRightLeft) or self.is_Zero_RL:

        # Se verifica que el semáforo al menos este encendido por minimo "x" steps y como máximo "y" steps.
        if ( (self.time_step_H == 0 and self.time_step_V < self.p.max_time_light)
            or (self.time_step_H >= self.p.min_time_light) ):
          
          self.time_step_H = 0
          self.time_step_V += 1

          # Se cambia el estado de color del semáforo.
          if self.dir == "horizontal":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde
        
        else:

          self.time_step_V = 0
          self.time_step_H += 1

          # Se cambia el estado de color del semáforo.
          if self.dir == "vertical":
            self.condition = 3 # Rojo
          else:
            self.condition = 2 # Verde


      # En caso de que no entre a ninguna condición, se queda con los mismos semáforos que estaban en verde y rojo.
      else:
        if (self.dir == "horizontal" and self.condition == 2) or (self.dir == "vertical" and self.condition == 3):
          self.time_step_V = 0
          self.time_step_H += 1
        elif (self.dir == "vertical" and self.condition == 2) or (self.dir == "horizontal" and self.condition == 3):
          self.time_step_H = 0
          self.time_step_V += 1



  """ Verifica e indica que carros pueden pasar y cuáles no. """
  def pass_car(self):
    
    ### Verificar que coches pueden manejar

    # Carril vertical
    if (self.dir == "horizontal" and self.condition == 2) or (self.dir == "vertical" and self.condition == 3):

      # Se detienen los carros correspondientes.
      for car in self.model.agents:
        if ((car.dir == 0) or
            (car.dir == 1 and car.side == 0 and
            (self.grid.positions[car][0] <= int(self.p.gridsize/2-3) or
            self.grid.positions[car][0] >= int(self.p.gridsize/2-1))) or
            (car.dir == 1 and car.side == 1 and
            (self.grid.positions[car][0] >= int(self.p.gridsize/2+4) or
            self.grid.positions[car][0] <= int(self.p.gridsize/2+2)))):
          car.condition = 0
        else:
          car.condition = 1

    # Carril horizontal
    elif (self.dir == "vertical" and self.condition == 2) or (self.dir == "horizontal" and self.condition == 3):
      # Se detienen los carros correspondientes.
      for car in self.model.agents:
        if ((car.dir == 1) or
            (car.dir == 0 and car.side == 0 and
            (self.grid.positions[car][1] <= int(self.p.gridsize/2-3) or
              self.grid.positions[car][1] >= int(self.p.gridsize/2-1))) or
            (car.dir == 0 and car.side == 1 and
            (self.grid.positions[car][1] >= int(self.p.gridsize/2+4) or
              self.grid.positions[car][1] <= int(self.p.gridsize/2+2)))):
          car.condition = 0
        else:
          car.condition = 1



  """ Verifica e indica que carros deben de esperar si se encuentran delante del semáforo que acaba de cambiar de color. """
  def wait_car(self):

    ### Verificar que coches deben de esperar cuando el semáforo acaba de cambiar de luz a verde. 

    # Carril vertical
    if (self.dir == "horizontal" and self.condition == 2) or (self.dir == "vertical" and self.condition == 3):
      # Se detienen los carros correspondientes.
      for car in self.model.agents:
        # Para que espere un 1 step al semáforo si recientemente se encendió y esta en una posicion vecina al semáforo.
        if (car.dir == 0 and car.side == 0) and (self.grid.positions[car][0]+1 == self.grid.positions[self][0]) and (self.grid.positions[car][1]+1 == self.grid.positions[self][1]) and (self.time_step_H <= 2):
          car.condition = 1
        elif (car.dir == 0 and car.side == 1) and (self.grid.positions[car][0]-1 == self.grid.positions[self][0]) and (self.grid.positions[car][1]-1 == self.grid.positions[self][1]) and (self.time_step_H <= 2):
          car.condition = 1

    # Carril horizontal
    elif (self.dir == "vertical" and self.condition == 2) or (self.dir == "horizontal" and self.condition == 3):
      # Se detienen los carros correspondientes.
      for car in self.model.agents:
        # Para que espere un 1 step al semáforo si recientemente se encendió y esta en una posicion vecina al semaforó.
        if (car.dir == 1 and car.side == 0) and (self.grid.positions[car][0]+1 == self.grid.positions[self][0]) and (self.grid.positions[car][1]-1 == self.grid.positions[self][1]) and (self.time_step_V <= 2):
          car.condition = 1
        elif (car.dir == 1 and car.side == 1) and (self.grid.positions[car][0]-1 == self.grid.positions[self][0]) and (self.grid.positions[car][1]+1 == self.grid.positions[self][1]) and (self.time_step_V <= 2):
          car.condition = 1



class IntersectionModel(ap.Model):
    
  """ Initialize the agents and network of the model. """
  def setup(self):

    gridsize = self.p['gridsize']

    rng = self.model.random

    self.grid = ap.Grid(self, (self.p.gridsize+1, self.p.gridsize+1), torus = True, track_empty= True)

    # Agentes Carros (Car)
    self.agents = ap.AgentList(self, 1, Car)
    if 0.5 > rng.random():
      self.grid.add_agents(self.agents, [(int(self.p.gridsize/2),self.p.gridsize)])
    else:
      self.grid.add_agents(self.agents, [(int(self.p.gridsize/2+1),0)])

    # Agentes Semáforos (TLight)
    self.semaforo = ap.AgentList(self, 4, TLight)
    self.grid.add_agents(self.semaforo, positions = [
      (int((gridsize/2)-1), int((gridsize/2)+2)), # Arriba-Derecha    -    Horizontal
      (int((gridsize/2)+2), int((gridsize/2)-1)), # Abajo-Izquierda   -    Horizontal
      (int((gridsize/2)-1), int((gridsize/2)-1)), # Arriba-Izquierda  -    Vertical
      (int((gridsize/2)+2), int((gridsize/2)+2))  # Abajo-Derecha     -    Vertical
    ])

    # Se les asigna a los semáforos cuales son para los carriles verticales.
    self.semaforo[2].dir = "vertical"
    self.semaforo[3].dir = "vertical"

    # Se les asigna a los semáforos sus respectivos id's.
    count_id_s = 0
    for tf in self.semaforo:
        tf.id = count_id_s
        count_id_s += 1

    # Para la recolección de datos.
    self.json = {}

    parameters = {}
    parameters["gridsize"] = gridsize
    parameters["cars"] = self.p.cars
    parameters["steps"] = self.p.steps
    parameters["turn_chance"] = self.p.turn_chance
    parameters["car_chance"] = self.p.car_chance
    parameters["min_time_light"] = self.p.min_time_light
    parameters["max_time_light"] = self.p.max_time_light

    self.json["parameters"] = parameters

    self.step_total = []

    step = {}

    step_car = []
    for car in self.agents:
      new_pos = {}
      new_pos["id"] = car.id
      new_pos["x"] = self.grid.positions[car][1]
      new_pos["y"] = self.grid.positions[car][0]

      if(self.grid.positions[car] == (int(self.p.gridsize/2),self.p.gridsize)):
        new_pos["new"] = "right"
      elif (self.grid.positions[car] == (int(self.p.gridsize/2+1),0)):
        new_pos["new"] = "left"
      elif (self.grid.positions[car] == (0, int(self.p.gridsize/2))):
        new_pos["new"] = "top"
      elif (self.grid.positions[car] == (self.p.gridsize, int(self.p.gridsize/2+1))):
        new_pos["new"] = "bot"
      else:
        new_pos["new"] = "not"

      step_car = np.append(step_car,new_pos)

    step_tf = []

    for tf in self.semaforo:
      new_light = {}
      new_light["id"] = tf.id
      new_light["light"] = 0 if tf.condition == 2 else 1
      step_tf = np.append(step_tf,new_light)

    step_tf = step_tf.tolist()
    step_car = step_car.tolist()

    step["car"] = step_car
    step["traffic_light"] = step_tf

    self.step_total = np.append(self.step_total,step)



  """ Define the models' events per simulation step. """
  def step(self):

    # Realiza los cálculos de tráfico.
    self.semaforo.calculate()

    # Manda la orden para cambiar la luz de los semáforos dependiendo las circunstancias.
    self.semaforo.change_light()

    # El semáforo le dice a los carros cuales pueden o no pasar.
    self.semaforo.pass_car()

    # El semáforo le dice a los carros cuáles deben de esperar por el cambio de luz.
    self.semaforo.wait_car()

    # Manda la orden para checar que no hayan carros vecinos y choquen.
    self.agents.check_neighbor()

    # Manda la orden de que todos los carros manejen si lo tienen permitido.
    self.agents.drive()

    # Agrega mas carros de manera aleatoria si entra dentro del rango permitido.
    rng = self.model.random
    if self.p.car_chance > rng.random() and len(self.agents) < self.p.cars: 
      self.new_agents = ap.AgentList(self, 1, Car)
      self.agents.extend(self.new_agents)
      if 0.5 > rng.random():
        if 0.5 > rng.random():
          self.grid.add_agents(self.new_agents, [(int(self.p.gridsize/2),self.p.gridsize)], empty=True)
        else:
          self.grid.add_agents(self.new_agents, [(int(self.p.gridsize/2+1),0)], empty=True)
      else:
        if 0.5 > rng.random():
          self.grid.add_agents(self.new_agents, [(0, int(self.p.gridsize/2))], empty=True)      
        else:
          self.grid.add_agents(self.new_agents, [(self.p.gridsize, int(self.p.gridsize/2+1))], empty=True)
      # Le asigna su respectivo id.
      self.agents[len(self.agents)-1].id = len(self.agents)-1
    
    step = {}

    step_car = []

    for car in self.agents:
      new_pos = {}
      new_pos["id"] = car.id
      new_pos["x"] = self.grid.positions[car][1]
      new_pos["y"] = self.grid.positions[car][0]

      if(self.grid.positions[car] == (int(self.p.gridsize/2),self.p.gridsize)):
        new_pos["new"] = "right"
      elif (self.grid.positions[car] == (int(self.p.gridsize/2+1),0)):
        new_pos["new"] = "left"
      elif (self.grid.positions[car] == (0, int(self.p.gridsize/2))):
        new_pos["new"] = "top"
      elif (self.grid.positions[car] == (self.p.gridsize, int(self.p.gridsize/2+1))):
        new_pos["new"] = "bot"
      else:
        new_pos["new"] = "not"
      
      step_car = np.append(step_car,new_pos)

    step_tf = []

    for tf in self.semaforo:
      new_light = {}
      new_light["id"] = tf.id
      new_light["light"] = 0 if tf.condition == 2 else 1
      step_tf = np.append(step_tf,new_light)

    step_tf = step_tf.tolist()
    step_car = step_car.tolist()

    step["car"] = step_car
    step["traffic_light"] = step_tf

    self.step_total = np.append(self.step_total,step)

  """ Define the end of the simulation. """
  def end(self):
    self.step_total = self.step_total.tolist()

    self.json["step"] = self.step_total

    with open('json_data.json', 'w') as file:
      json.dump(self.json, file, indent = 2)