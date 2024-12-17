import turtle
from PIL import Image, ImageSequence
import os

def inicializar_turtle(ancho, alto):
    """
    Configura la ventana y el entorno de Turtle.
    :param ancho: Ancho de la ventana.
    :param alto: Alto de la ventana.
    """
    turtle.setup(width=ancho, height=alto)
    turtle.setworldcoordinates(0, 0, ancho, alto)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.tracer(False)
    turtle.bgcolor("white")

def dibujar_cuadro(x, y, tamano, color, rellenar=True):
    """
    Dibuja un cuadro con un borde negro explícito y opcionalmente con relleno de color.
    :param x: Coordenada x de inicio.
    :param y: Coordenada y de inicio.
    :param tamano: Tamaño del cuadro.
    :param color: Color del cuadro.
    :param rellenar: Booleano que indica si se rellena el cuadrado.
    """
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    
    # Configurar borde negro
    turtle.pencolor("black")
    turtle.width(1)
    
    if rellenar:
        # Dibujar cuadro con relleno de color
        turtle.fillcolor(color)
        turtle.begin_fill()
    
    for _ in range(4):
        turtle.forward(tamano)
        turtle.left(90)
    
    if rellenar:
        turtle.end_fill()



def guardar_frame(nombre):
    """
    Guarda un frame actual de Turtle como archivo .eps.
    :param nombre: Nombre del archivo .eps.
    """
    canvas = turtle.getcanvas()
    canvas.postscript(file=nombre)

def convertir_a_gif(nombre_base, nombre_gif, duracion, num_frames):
    """
    Convierte una serie de archivos .eps a un GIF animado sin bordes blancos.
    :param nombre_base: Nombre base de los archivos .eps.
    :param nombre_gif: Nombre del archivo GIF de salida.
    :param duracion: Duración de cada cuadro en ms.
    :param num_frames: Número de cuadros.
    """
    frames = []
    for i in range(num_frames):
        # Cargar la imagen EPS
        img = Image.open(f"{nombre_base}_{i}.eps")
        img = img.convert("RGBA")
        
        # Recortar los bordes blancos
        img = img.crop(img.getbbox())
        
        # Convertir el fondo blanco en transparente
        datas = img.getdata()
        new_data = []
        for item in datas:
            # Reemplazar el blanco puro con transparente
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))  # Transparente
            else:
                new_data.append(item)
        img.putdata(new_data)
        
        frames.append(img)

    # Guardar como GIF
    frames[0].save(
        nombre_gif,
        save_all=True,
        append_images=frames[1:],
        duration=duracion,
        loop=0
    )
    print(f"GIF guardado como {nombre_gif}")


def main():
    # Configuración
    ANCHO = 400
    ALTO = 400
    TAMANO_CUADRO = 30
    #Aqui cambiar los colores :)
    COLORES = ["#FFFEEC", "#187498", "#F9D923", "#EB5353", "#36AE7C"]
    NUM_FRAMES = 15
    DURACION = 150 # Duración en milisegundos
    NOMBRE_BASE = "frame"
    NOMBRE_GIF = "mosaico_infinito.gif"

    # Inicializar Turtle
    inicializar_turtle(ANCHO, ALTO)

    # Dibujar y guardar frames
    for i in range(NUM_FRAMES):
        turtle.clear()
        offset = (i * TAMANO_CUADRO // 2) % TAMANO_CUADRO  # Desplazamiento infinito
        
        for y in range(0, ALTO, TAMANO_CUADRO):
            for x in range(-offset, ANCHO, TAMANO_CUADRO):
                color = COLORES[(x // TAMANO_CUADRO + y // TAMANO_CUADRO + i) % len(COLORES)]
                dibujar_cuadro(x, y, TAMANO_CUADRO, color)
        
        # Dibujar último borde (sin relleno) para cerrar posibles desfases
        dibujar_cuadro(-offset + ANCHO, 0, TAMANO_CUADRO, color, rellenar=False)
        
        guardar_frame(f"{NOMBRE_BASE}_{i}.eps")
        print(f"Guardado frame {i+1}/{NUM_FRAMES}")


    # Convertir los frames a GIF
    convertir_a_gif(NOMBRE_BASE, NOMBRE_GIF, DURACION, NUM_FRAMES)

    # Limpiar archivos temporales
    for i in range(NUM_FRAMES):
        os.remove(f"{NOMBRE_BASE}_{i}.eps")
    print("Archivos temporales eliminados.")

    turtle.done()
    os.kill()

if __name__ == "__main__":
    main()
