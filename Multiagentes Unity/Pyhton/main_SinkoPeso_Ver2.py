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
          and self.dir == 1 and self.side == 0) and 
          self.p.turn_chance > rng.random()): # street is Turnable (V-R)
        self.dir = 0
        self.side = 1
      elif ((self.grid.positions[self] == (int(self.p.gridsize/2),int(self.p.gridsize/2+1))
          and self.dir == 0 and self.side == 1) and 
          self.p.turn_chance > rng.random()): # street is Turnable (H-L)
        self.dir = 1
      elif ((self.grid.positions[self] == (int(self.p.gridsize/2+1),int(self.p.gridsize/2))
          and self.dir == 0 and self.side == 0) and 
          self.p.turn_chance > rng.random()): # street is Turnable (H-R)
        self.dir = 1
      elif ((self.grid.positions[self] == (int(self.p.gridsize/2+1),int(self.p.gridsize/2+1))
          and self.dir == 1 and self.side == 1) and 
          self.p.turn_chance > rng.random()): # street is Turnable (V-L)
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
    
  def setup(self):
    self.condition = 2          # Rojo = 2, Verde = 3
    self.grid = self.model.grid
    self.id = 0

      
  def change_light(self):
    
    # Contador para el tráfico total.
    traffic = 0

    # Contadores para los carriles.
    countRightLeft = 0
    countUpDown = 0

    # Verfica que no este vacio uno de los contadores.
    is_Zero_RL = True
    is_Zero_UD = True

    # Obtiene la menor distancia desde la posición de un carro hasta al cruce del carril horizontal.
    minH = self.p.gridsize
    # Obtiene la menor distancia desde la posición de un carro hasta al cruce del carril vertical.
    minV = self.p.gridsize




    ### CALCULOS

    for car in self.model.agents:

      # HORIZONTAL & DERECHA/IZQUIERDA
      if ((car.dir == 0 and car.side == 0 and self.grid.positions[car][1] >= 0 and
          self.grid.positions[car][1] <= int(self.p.gridsize/2-2)) or
          (car.dir == 0 and car.side == 1 and self.grid.positions[car][1] >= int(self.p.gridsize/2+3) and
          self.grid.positions[car][1] <= self.p.gridsize)):
        
        countRightLeft += 1

        traffic += 1
        
        is_Zero_RL = False

        aux = self.p.gridsize

        if (car.side == 0 and self.grid.positions[car][1] >= 0 and
            self.grid.positions[car][1] <= int(self.p.gridsize/2-2)):
          aux = int(self.p.gridsize/2) - 2 - self.grid.positions[car][1]
        elif (car.side == 1 and self.grid.positions[car][1] >= int(self.p.gridsize/2+3) and
            self.grid.positions[car][1] <= self.p.gridsize):
          aux = self.grid.positions[car][1] - int(self.p.gridsize/2) - 3

        if aux < minH:
          minH = aux

      # VERTICAL & ABAJO/ARRIBA
      elif ((car.dir == 1 and car.side == 0 and self.grid.positions[car][0] >= 0 and
          self.grid.positions[car][0] <= int(self.p.gridsize/2-2)) or
          (car.dir == 1 and car.side == 1 and self.grid.positions[car][0] >= int(self.p.gridsize/2+3) and
          self.grid.positions[car][0] <= self.p.gridsize)):
        
        countUpDown += 1

        traffic += 1

        is_Zero_UD = False

        aux = self.p.gridsize

        if (car.side == 0 and self.grid.positions[car][0] >= 0 and
            self.grid.positions[car][0] <= int(self.p.gridsize/2-2)):
          aux = int(self.p.gridsize/2) - 2 - self.grid.positions[car][0]
        elif (car.side == 1 and self.grid.positions[car][0] >= int(self.p.gridsize/2+3) and
            self.grid.positions[car][0] <= self.p.gridsize):
          aux = self.grid.positions[car][0] - int(self.p.gridsize/2) - 3

        if aux < minV:
          minV = aux




    ### VERIFICACIONES PARA CAMBIAR DE COLOR LAS LUCES

    # Si es poco trafico
    if traffic < 10:
      # Verifica si en el carril horizontal hay un carro más cerca que el del vertical.
      if minH < minV:
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if ((self.model.time_step_V == 0 and
            (((self.id == 0 or self.id == 1 or self.id == 2) and
            self.model.time_step_H < self.p.max_time_light) or
            (self.id == 3 and self.model.time_step_H <= self.p.max_time_light))) or
            ((self.id == 0 and self.model.time_step_V >= self.p.min_time_light) or
            ((self.id == 1 or self.id == 2 or self.id == 3)
            and self.model.time_step_V > self.p.min_time_light))):
          
          self.model.time_step_V = 0
            
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

        else:
          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

      # Verifica si en el carril vertical hay un carro más cerca que el del horizontal.
      elif minV < minH:
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if (((self.model.time_step_H == 0 and
            ((self.id == 0 and self.model.time_step_V < self.p.max_time_light) or
            ((self.id == 1 or self.id == 2 or self.id == 3) and
            self.model.time_step_V <= self.p.max_time_light and
            self.model.semaforo[0].condition == 3) ) ) or
            ((self.id == 2 or self.id == 0 or self.id == 1) and
            self.model.time_step_H >= self.p.min_time_light) or
            (self.id == 3 and self.model.time_step_H > self.p.min_time_light))):

          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo
        
        else:
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

      # Verifica si en el carril horizontal hay menos tráfico
      elif (not is_Zero_RL and countRightLeft < countUpDown) or is_Zero_UD:
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if ((self.model.time_step_V == 0 and
            (((self.id == 0 or self.id == 1 or self.id == 2) and
            self.model.time_step_H < self.p.max_time_light) or
            (self.id == 3 and self.model.time_step_H <= self.p.max_time_light))) or
            ((self.id == 0 and self.model.time_step_V >= self.p.min_time_light) or
            ((self.id == 1 or self.id == 2 or self.id == 3) and
            self.model.time_step_V > self.p.min_time_light))):
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

        else:
          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

      # Verifica si en el carril vertical hay menos tráfico
      elif (not is_Zero_UD and countUpDown < countRightLeft) or is_Zero_RL:
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if (self.model.time_step_H == 0 and ( (self.id == 0 and self.model.time_step_V < self.p.max_time_light) or 
            ( (self.id == 1 or self.id == 2 or self.id == 3) and self.model.time_step_V <= self.p.max_time_light and 
            self.model.semaforo[0].condition == 3) ) ) or ( ( (self.id == 2 or self.id == 0 or self.id == 1) and 
            self.model.time_step_H >= self.p.min_time_light) or (self.id == 3 and self.model.time_step_H > self.p.min_time_light) ):

          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

        else:
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

    # Si es mucho trafico
    else:
      # Verifica si en el carril horizontal hay un carro más cerca que el del vertical.
      if minH < minV:
        #self.p.min_time_light += countUpDown
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if ((self.model.time_step_V == 0 and
            (((self.id == 0 or self.id == 1 or self.id == 2) and
            self.model.time_step_H < self.p.max_time_light) or
            (self.id == 3 and self.model.time_step_H <= self.p.max_time_light))) or
            ((self.id == 0 and self.model.time_step_V >= self.p.min_time_light) or
            ((self.id == 1 or self.id == 2 or self.id == 3) and
            self.model.time_step_V > self.p.min_time_light))):
          
          self.model.time_step_V = 0
            
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

        else:
          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

      # Verifica si en el carril vertical hay un carro más cerca que el del horizontal.
      elif minV < minH:
        #self.p.min_time_light += countRightLeft
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if ((self.model.time_step_H == 0 and
            ((self.id == 0 and self.model.time_step_V < self.p.max_time_light) or
            ((self.id == 1 or self.id == 2 or self.id == 3) and
            self.model.time_step_V <= self.p.max_time_light and
            self.model.semaforo[0].condition == 3))) or
            (((self.id == 2 or self.id == 0 or self.id == 1) and
            self.model.time_step_H >= self.p.min_time_light) or
            (self.id == 3 and self.model.time_step_H > self.p.min_time_light))):

          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo
        
        else:
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

      # Verifica si en el carril horizontal hay menos tráfico
      elif (not is_Zero_RL and countRightLeft > countUpDown) or is_Zero_UD:
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if ((self.model.time_step_V == 0 and
            (((self.id == 0 or self.id == 1 or self.id == 2) and
            self.model.time_step_H < self.p.max_time_light) or
            (self.id == 3 and self.model.time_step_H <= self.p.max_time_light))) or
            ((self.id == 0 and self.model.time_step_V >= self.p.min_time_light) or 
            ((self.id == 1 or self.id == 2 or self.id == 3) and
            self.model.time_step_V > self.p.min_time_light))):

          self.model.time_step_V = 0

          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

        else:
          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

      # Verifica si en el carril vertical hay menos tráfico
      elif (not is_Zero_UD and countUpDown > countRightLeft) or is_Zero_RL:
        # Se verifica que el semaforo al menos este encendido por minimo 5 steps
        if ((self.model.time_step_H == 0 and
            ((self.id == 0 and self.model.time_step_V < self.p.max_time_light) or
            ((self.id == 1 or self.id == 2 or self.id == 3) and
            self.model.time_step_V <= self.p.max_time_light and
            self.model.semaforo[0].condition == 3))) or
            (((self.id == 2 or self.id == 0 or self.id == 1) and
            self.model.time_step_H >= self.p.min_time_light) or
            (self.id == 3 and self.model.time_step_H > self.p.min_time_light))):

          # Se cambia el estado de color del semaforo
          if self.id == 0 or self.id == 1:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo

        else:
          # Se cambia el estado de color del semaforo
          if self.id == 2 or self.id == 3:
            self.condition = 3 # Verde
          else:
            self.condition = 2 # Rojo




    ### Verificar que coches pueden manejar

    # Carril horizontal
    if self.id == 2 and self.condition == 3:
      # Tiempo por cada semaforo
      self.model.time_step_H += 1
      self.model.time_step_V = 0
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

    # Carril vertical
    elif self.id == 0 and self.condition == 3:
      # Tiempo por cada semaforo
      self.model.time_step_V += 1
      self.model.time_step_H = 0
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

    self.time_step_H = 0
    self.time_step_V = 0

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

    # Manda la orden para cambiar la luz de los semáforos dependiendo las circunstancias.
    self.semaforo.change_light()

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

  def end(self):
    self.step_total = self.step_total.tolist()

    self.json["step"] = self.step_total

    with open('json_data.json', 'w') as file:
      json.dump(self.json, file, indent = 2)