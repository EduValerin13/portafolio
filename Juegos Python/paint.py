"""Paint, for drawing shapes.

Exercises

1. Add a color.
2. Complete circle.
3. Complete rectangle.
4. Complete triangle.
5. Add width parameter.

"""

from turtle import *

from freegames import vector

import math

# Función que despliega nuestros nombres
def info_alumnos():
    writer.up()
    writer.goto(0,190)
    writer.color('blue')
    writer.write('Eduardo Andrés Valerin Vijil', align = 'left', font = ('Arial',10,'normal'))
    writer.goto(0,170)
    writer.color('red')
    writer.write('Gabriel Eduardo Diaz Roa', align = 'left', font = ('Arial',10,'normal'))

# Función que dibuja una linea
def line_paint(start, end):
    "Draw line from start to end."
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)

# Función que dibuja un cuadrado
def square_paint(start, end):
    "Draw square from start to end."
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(4):
        forward(end.x - start.x)
        left(90)

    end_fill()

# Función que dibuja un circulo
def circle_paint(start, end):
    up()
    goto(start.x,start.y)
    goto(end.x, end.y)
    down()
    radius=(math.sqrt(((end.x-start.x)**2)+((end.y-start.y)**2)))*-1
    begin_fill()
    circle(radius)
    end_fill()

# Función que dibuja un rectangulo
def rectangle_paint(start, end):
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(2):
        forward(end.x - start.x)
        left(90)
        forward(end.y - start.y)
        left(90)

    end_fill()

# Función que dibuja un triangulo
def triangle_paint(start, end):
    "Draw triangle from start to end."
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(3):
        forward(end.x - start.x)
        left(120)

    end_fill()

# Función tap que recibe las coordenadas (x,y) del click realizado
def tap(x, y):
    "Store starting point or draw shape."
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)
    else:
        shape = state['shape']
        end = vector(x, y)
        shape(start, end)
        state['start'] = None

# Función que recibe el tipo (figura) y la función de la figura
def store(key, value):
    "Store value in state at key."
    state[key] = value

# Diccionario
state = {'start': None, 'shape': line_paint}

# Crea Objeto Ventana que comienza en (0,0)
setup(width=420, height=420, startx=0, starty=0)

# Llama a la funcion tap(x,y) cuando el usuario da click sobre la ventana
onscreenclick(tap)

# Escucha todos los eventos, funciona como una oreja del programa
listen()

writer = Turtle(visible=False)

# Llama a la función alumnos
info_alumnos()

# Tecla para deshacer los cambios realizados
onkey(undo, 'u')
onkey(undo, 'U')

# Elige el color de la figura
onkey(lambda: color('black'), 'k')
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'w')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'g')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'b')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'r')
onkey(lambda: color('red'), 'R')
onkey(lambda: color('orange'), 'o')
onkey(lambda: color('orange'), 'O')

# Elige la figura haciendo uso de la función sin parametros lambda
onkey(lambda: store('shape', line_paint), 'l')
onkey(lambda: store('shape', line_paint), 'L')
onkey(lambda: store('shape', square_paint), 's')
onkey(lambda: store('shape', square_paint), 'S')
onkey(lambda: store('shape', circle_paint), 'c')
onkey(lambda: store('shape', circle_paint), 'C')
onkey(lambda: store('shape', rectangle_paint), 'e')
onkey(lambda: store('shape', rectangle_paint), 'E')
onkey(lambda: store('shape', triangle_paint), 't')
onkey(lambda: store('shape', triangle_paint), 'T')

# Inicia los eventos
done()