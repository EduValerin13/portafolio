from random import *
from turtle import *
from freegames import path

car = path('car.gif') # Imagen del carro que se encuentra atras de los cuadros
txt = '''Ferrari&Bugatti&Lamborghini&Audi&Subaru&Lexus&Porsche&BMW&Mazda&Buick
&Toyota&Kia&Honda&Hyundai&Volvo&Mini&Mercedes-Benz&Volkswagen&Ford&Lincoln&Scion
&Acura&Chevrolet&Nissan&Infiniti&GMC&Cadillac&Dodge&Land Rover&Mitsubishi&Jeep&Fiat''' # String con la lista de automoviles
tiles = txt.split("&") * 2 # Dividimos el string separado por & en una lista y lo multiplicamos por 2
state = {'mark': None} # No se ha selecionado ningun cuadro
taps = 0 # Inicializamos los taps (clicks)
hide = [True] * 64 # Se inicializan una lista de 64 valores True como escondidos
ancho = 50 # Ancho y largo del cuadro

# Función que dibuja los cuadrados
def square(x, y):
    "Draw white square with black outline at (x, y)."
    up() # Levanta el lapiz
    goto(x, y) # Va hacia la posicion indicada
    down() # Baja el lapiz
    color('black', 'blue') # Elige un color negro para las orillas y azul para rellenar
    begin_fill() # Empieza a dibujar
    
    # Ciclo for que se ejecuta cuatro veces
    for count in range(4): 
        forward(ancho) # avanza 50 espacios adelante
        left(90) # gira hacia la izquierda en 90 grados
        
    end_fill() # Termina de dibujar y rellenar

# Función que calcula el index del tap realizado
def index(x, y):
    "Convert (x, y) coordinates to tiles index."
    return int((x + 200) // ancho + ((y + 200) // ancho) * 8)

# Convierte el index a coordenadas (x,y)
def xy(count):
    "Convert tiles count to (x, y) coordinates."
    return (count % 8) * ancho - 200, (count // 8) * ancho - 200

# Función para taps
def tap(x, y):
    # Variables globales
    global mark, taps, escondidas
    
    # Actualizamos la variable taps en una unidad para contar los clicks
    taps = taps + 1
    
    "Update mark and hidden tiles based on tap."
    spot = index(x, y) # Busca el index del click realizado
    mark = state['mark'] # Se encuentra selecionado un cuadro
    
    # Condicional que verifica si mark es None o si mark es igual a spot
    # o si el titulo de mark no es igual al titulo de spot
    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    
    # Si no se cumple significa que los 2 titulos son iguales
    else:
        hide[spot] = False # Ya no se muestra el cuadro
        hide[mark] = False # Ya no se muestra el cuadro
        state['mark'] = None # Ya no hay un cuadro seleccionado

# Función que grafica los cuadros
def draw():
    "Draw image and tiles."
    clear() # Limpia la ventana
    goto(0,0) # Va hacia la posición (0,0)
    shape(car) # Encuentra la figura del carro
    stamp() # Despliega la figura del carro
    
    # Ciclo for que se ejecuta 64 para dibujar los cuadros que no estan escondidos
    for count in range(64):
        # Verifica si el cuadro no esta escondido (True)
        if hide[count]:
            x,y = xy(count) # Convierte el index a coordenadas x,y
            square(x,y) # Llama a la función square
    
    # El cuadro sigue marcado
    mark = state['mark']
    
    # Verifica si mark no es None y si no esta escondido
    if mark is not None and hide[mark]:
        x,y = xy(mark) # Convierte el index a coordenadas x,y
        up() # Levanta el lapiz
        goto(x + 27, y + 20) # Va hacia la dirección indicada, sumandole 27 unidades en x y 20 unidades en y
        color('white') # Cambia el color a blanco
        # Escribe el titulo seleccionado de la lista
        write(tiles[mark], font=('Arial', 8, 'normal'),align = 'center')
    
    # Se cuentan cuantos cuadros siguen escondiendo la imagen del carro
    escondidas = hide.count(True)
    
    # Verifica si ya se termino el juego
    if escondidas == 0:
        up() # Levanta el lapiz
        goto(0,150) # Va hacia esta posición
        color('red') # Elige el color rojo
        write('GANASTE UN AUTO',font=('Arial',20,'normal'),align = 'center') # Escribe el mensaje
        color('white') # Elige el color blanco
        goto(0,100) # Va hacia esta posición
        write('¡Felicidades!',font=('Arial',20,'normal'),align = 'center') # Escribe el mensaje
        color('black') # Elige el color negro
        goto(0,-150) # Va hacia esta posición
        # Escribe cuantos taps se hicieron
        write(f'Hiciste {taps} taps',font=('Arial',15,'normal'),align = 'center')

    update() # Actualiza la ventana
    ontimer(draw, 100) # Velocidad del dibujo

# Revuelve los titulos aleatoriamente
shuffle(tiles)

# Crea una ventana que comienza en (370,0) desde la esquina izquierda
setup(420, 420, 370, 0)

# Agrega la figura del carro
addshape(car)

# Esconder el > (Turtle)
hideturtle()

# No muestra el graficado de cada elemeto en la ventana
tracer(False)

# Llama a la función tap y se le envian las coordenadas del click realizado
onscreenclick(tap)

# Llama a la función draw
draw()

# Inicia los eventos
done()