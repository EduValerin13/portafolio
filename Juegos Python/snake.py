from turtle import *
from random import randrange, choice
from freegames import square, vector

food = vector(0,0) # Posición inicial de la comida
snake = [vector(10, 0)] # Lista con el tamaño y posiciones del snake
aim = vector(0, -10) # En que dirección va el snake
movimientos_food = [vector(-10,0),vector(10,0),vector(0,-10),vector(0,10)] # Posibles movimientos aleatorios de la comida
lista_colores = ['blue','yellow','turquoise','green','orange','gold','lightgreen'] # Lista de colores para la comida y el snake
color_snake = choice(lista_colores) # Elige un color aleatorio de la lista de colores para el snake
lista_colores.remove(color_snake) # Elimina el color elegido para el snake
color_food = choice(lista_colores) # Elige un color aleatorio de la lista de colores para la comida

# Escriba nuestros nombres
def info_alumnos():
    writer.up()
    writer.goto(-5,190)
    writer.color('maroon')
    writer.write('Eduardo Andrés Valerin Vijil', align = 'left', font = ('Arial',10,'normal'))

# Cambia la direcion del snake
def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

# Verifica que la cabeza del snake este dentro de los limites establecidos
def inside(head):
    "Return True if head inside boundaries."
    return -210 < head.x < 190 and -200 < head.y < 200

# Verifica que la comida este dentro de los limites establecidos
def inside_food(food):
    "Return True if food inside boundaries."
    return -180 < food.x < 180 and -180 < food.y < 180

# Función move
def move():
    # Variables globales
    global color_snake, color_food, lista_colores, food, vuelta
    
    "Move snake forward one segment."
    # Crea una copia del vector que esta en la ultima posición de la lista
    head = snake[-1].copy()
    head.move(aim)
    
    # Verifica si la cabeza del snake no esta dentro de los limites (choco con los limites) o si la posición
    # de la cabeza nueva se encuentra dentro de la lista del tamaño del snake (choco con su propio cuerpo)
    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red') # Si se cumple una de las condiciones cambia a color rojo la cabeza nueva del snake
        writer.up()
        writer.goto(0,0) # Se coloca en la posicion (0,0) para escribir
        writer.color('red') # Escribe en color rojo
        # Escribe GAME OVER, alineado en el centro y con un font Arial con tamaño 25
        writer.write('GAME OVER', align = 'center', font = ('Arial',25,'normal'))
        update()
        return
    
    # Simula el movimiento si no se cumple ninguna de las 2 condiciones
    snake.append(head)
    
    # Verifica si la cabeza llega a la comida
    if head == food:
        print('Tamaño del Snake:', len(snake)) # Imprime el nuevo tamaño del snake
        food.x = randrange(-15, 15) * 10 # Cambia aleatoriamente la posicion en x de la comida en un rango de -15 a 15
        food.y = randrange(-15, 15) * 10 # Cambia aleatoriamente la posicion en y de la comida en un rango de -15 a 15
    else:
        snake.pop(0) # Si no llega a la comida se elimina el primer vector de la lista del tamaño del snake
    
    # Condicion que regula el movimiento de la comida
    if vuelta % 5 == 0:
        # Crea una copia de la posición de la comida
        food_aux = food.copy()
        
        # Mueve en 10 posiciones la copia aleatoriamente hacia arriba, abajo, izquierda o derecha
        food_aux.move(choice(movimientos_food))
    
        # Ciclo while que se ejecuta mientras la copia de la comida no este adentro de los limites o
        # si se encuentra dentro del cuerpo del snake
        while not inside_food(food_aux) or food_aux in snake:
            
            # Crea una nueva copia de la posición de la comida
            food_aux = food.copy()
        
            # Mueve en 10 posiciones la nueva copia aleatoriamente hacia arriba, abajo, izquierda o derecha
            food_aux.move(choice(movimientos_food))
        
        # Si la copia de la comida se encuentra dentro de los limites y no esta dentro del snake se
        # convierte en la nueva posicion de la comida
        food = food_aux
        
    # Actualiza la variable vuelta que cuenta cuantos espacios se ha movido el snake
    vuelta = vuelta + 1
    
    # Borra los dibujos de la pantalla
    clear()
    
    # Dibuja nuevamente el snake con sus nuevas posiciones y/o tamaño
    for body in snake:
        square(body.x, body.y, 9, color_snake)
        
    # Dibuja nuevamente la comida con su nueva posicion
    square(food.x, food.y, 9, color_food)
    update()
    ontimer(move, 500) # Velocidad con la que se mueve el snake y la comida

# Crea una ventana que comienza en 0,0 desde la esquina izquierda
setup(width=420, height=420, startx=0, starty=0)

# Esconder el > (Turtle)
hideturtle()

# No muestra el graficado de cada elemeto en la ventana
tracer(False)

# Escucha todos los eventos, funciona como una oreja del programa
listen()

# Cambia el color del background
bgcolor('#9FAAA8')

# Hace no visible el turtle
writer = Turtle(visible=False)

# Llama a la funcion alumnos (Despliega nuestros nombres)
info_alumnos()

# Inicializamos la vuelta
vuelta = 0

# Recibe una tecla y cambia su direccion haciendo uso de la funcion sin parametros lambda

# Usando las flechas
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

# Usando WASD
onkey(lambda: change(0, 10), 'w')
onkey(lambda: change(0, 10), 'W')
onkey(lambda: change(-10, 0), 'a')
onkey(lambda: change(-10, 0), 'A')
onkey(lambda: change(0, -10), 's')
onkey(lambda: change(0, -10), 'S')
onkey(lambda: change(10, 0), 'd')
onkey(lambda: change(0, -10), 'D')

# Llama a la funcion move
move()

# Inicia los eventos
done()