from PIL import Image, ImageDraw
import random
import math
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


def validate_hex_color(color):
    """
    Valida si un color ingresado está en formato hexadecimal.
    """
    if len(color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in color):
        return True
    return False


'''
def get_user_input():
    
    #Solicita los parámetros al usuario con una interfaz mejorada usando Rich.
   
    # Introducción al procedimiento
    descripcion = """[bold green]🎨 [bold white]Bienvenido al[/bold white] Generador de GIFs Procedural![/bold green]

[bold green]Procedimiento para Generar un GIF Procedural:[/bold green] 

    1. [bold magenta]Escoger el fondo:[/bold magenta] El usuario deberá escoger el fondo, el cual puede o no tener un color. 
       Si se elige un fondo sin color, el GIF será transparente. 
    
    2. [bold magenta]Seleccionar las figuras:[/bold magenta] El usuario podrá agregar las figuras que desee dentro del GIF. 
       Las opciones disponibles son cuadrado, círculo y triángulo. 
    
    3. [bold magenta]Definir la paleta de colores:[/bold magenta] El usuario deberá ingresar los colores en formato hexadecimal. 
       Se recomienda visitar [link=https://colorhunt.co]colorhunt.co[/link] para ver referencias y elegir colores atractivos.

    4. [bold magenta]Seleccionar la animación:[/bold magenta] ¡Escoge entre las opciones disponibles y diviértete!

¡Sigue estos pasos para crear tu GIF personalizado y disfruta del proceso creativo!"""
    console.print(Panel(descripcion))

    # Selección del fondo
    while True:
        background_choice = Prompt.ask(
            "\n🟪 ¿Deseas un [bold cyan]color de fondo[/bold cyan] o un [bold yellow]fondo transparente[/bold yellow] (escribe [bold cyan]color[/bold cyan] o [bold yellow]sin fondo[/bold yellow])",
            choices=["color", "sin fondo"]
        )
        if background_choice == "color":
            background_color = Prompt.ask("   Ingresa el [bold cyan]color de fondo[/bold cyan] en formato hexadecimal (ejemplo: FFFFFF)")
            if validate_hex_color(background_color):
                background_color = f"#{background_color}"
                break
            else:
                console.print("   [bold red]El color ingresado no es válido. Intenta nuevamente.[/bold red]")
        else:
            background_color = None
            break

    # Selección de figuras
    shapes = []
    console.print("\n🟪 Selecciona las [bold red]formas[/bold red] para incluir en el GIF(Circulos/Triangulos/Cuadrados):")
    if Prompt.ask("   ¿Círculos? 🔴", choices=["si", "no"]) == "si":
        shapes.append("circle")
    if Prompt.ask("   ¿Triángulos? 🔺", choices=["si", "no"]) == "si":
        shapes.append("triangle")
    if Prompt.ask("   ¿Cuadrados? 🟥", choices=["si", "no"]) == "si":
        shapes.append("rectangle")
    if not shapes:
        console.print("[bold yellow]No seleccionaste ninguna forma. Por defecto se usarán círculos.[/bold yellow]")
        shapes.append("circle")

    # Selección de colores
    palette = []
    console.print("\n🟪 Ingresa [bold blue]4 colores[/bold blue] para las figuras en formato hexadecimal:")
    for i in range(1, 5):
        while True:
            color = Prompt.ask(f"   [bold blue]Color {i}[/bold blue]:")
            if validate_hex_color(color):
                palette.append(f"#{color}")
                break
            else:
                console.print("   [bold red]El color ingresado no es válido. Intenta nuevamente.[/bold red]")

    return background_color, shapes, palette
'''


def draw_shape(draw, shape, x, y, size, color):
    """
    Dibuja una figura específica en el canvas.
    """
    # Coordenadas de la figura (centradas en x, y)
    x1, y1 = x - size // 2, y - size // 2
    x2, y2 = x + size // 2, y + size // 2

    # Dibuja la figura según el tipo
    if shape == "circle":  # Círculo
        draw.ellipse([x1, y1, x2, y2], fill=color)
    elif shape == "rectangle":  # Cuadrado
        draw.rectangle([x1, y1, x2, y2], fill=color)
    elif shape == "triangle":  # Triángulo
        draw.polygon([x1, y1, x2, y2, x, y - size], fill=color)


# ======== Animaciones ========

def generate_mosaic_animation(draw, frame, width, height, shapes, palette, size_range, total_frames):
    """
    Genera el marco para la animación 'Mosaico' con figuras fijas que no cambian de tamaño ni posición.
    Las figuras se distribuyen desde el centro hacia los bordes con un margen entre ellas.
    """
    center_x, center_y = width // 2, height // 2  # Centro del lienzo
    cell_size = max(size_range) // 2  # Tamaño de cada celda (más pequeñas)
    num_columns = width // cell_size  # Número de columnas en la cuadrícula
    num_rows = height // cell_size  # Número de filas en la cuadrícula

    # Calcula la distancia máxima desde el centro al borde del canvas
    max_distance = math.sqrt((center_x) ** 2 + (center_y) ** 2)

    # Lista para almacenar las posiciones y tamaños de las figuras
    active_shapes = []
    placed_positions = set()  # Para evitar superposición de figuras

    # Genera posiciones de las figuras y asegura que no se toquen
    for row in range(num_rows):
        for col in range(num_columns):
            # Calcula la posición de cada celda en la cuadrícula
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2

            # Asegurarse de que la figura no se superponga con otras
            if (x, y) not in placed_positions:
                # Selecciona una figura y un color aleatorio
                shape = random.choice(shapes)
                color = random.choice(palette)
                
                # Genera un tamaño entre el rango dado, pero las figuras serán más pequeñas
                size = random.randint(size_range[0] // 2, size_range[1] // 2)  # Tamaño más pequeño
                
                # Agregar la figura y marcar la posición como ocupada
                active_shapes.append((shape, x, y, size, color))
                placed_positions.add((x, y))

    # Dibuja las figuras activas (con tamaño constante)
    for shape, x, y, size, color in active_shapes:
        draw_shape(draw, shape, x, y, size, color)




"""
def generate_bubbles_animation(draw, frame, width, height, shapes, palette, size_range, total_frames):
    """
    # Genera el marco para la animación 'Burbujas'.
"""
    num_shapes = max(5, frame * 5 // total_frames)  # Número de figuras basado en el frame actual
    active_shapes = []  # Figuras que se dibujarán en este frame

    for _ in range(num_shapes):  # Dibujar figuras
        shape = random.choice(shapes)  # Tipo de figura
        color = random.choice(palette)  # Color
        size = random.randint(size_range[0], size_range[1])  # Tamaño
        x = random.randint(0, width)  # Posición aleatoria x
        y = random.randint(0, height)  # Posición aleatoria y
        active_shapes.append((shape, x, y, size, color))

    # Dibuja todas las figuras activas
    for shape, x, y, size, color in active_shapes:
        draw_shape(draw, shape, x, y, size, color)

def generate_spiral_animation(draw, frame, width, height, shapes, palette, size_range, total_frames):
    """
   # Genera el marco para la animación 'Espiral' con figuras que aparecen progresivamente,
   # están más separadas y desaparecen desde el inicio al final.
"""
    center_x, center_y = width // 2, height // 2  # Centro del lienzo
    num_figures = 100  # Número total de figuras en la espiral
    max_radius = min(width, height) // 2  # Radio máximo de la espiral
    spacing = 20  # Espaciado entre figuras (ajusta para más separación)
    active_shapes = []  # Figuras que se dibujarán en este frame

    # Control de las figuras visibles en función del frame
    visible_start = int((frame / total_frames) * num_figures)  # Inicio de figuras visibles
    visible_end = int(((frame + 1) / total_frames) * num_figures)  # Fin de figuras visibles

    for i in range(visible_start, visible_end):
        # Incremento dinámico para la animación
        angle = i * spacing / max_radius * 2 * math.pi  # Ángulo ajustado para más separación
        radius = spacing * i  # Incremento radial basado en el índice
        if radius > max_radius:  # Detener figuras fuera del rango del lienzo
            break

        x = center_x + int(radius * math.cos(angle))  # Coordenada x
        y = center_y + int(radius * math.sin(angle))  # Coordenada y

        # Seleccionar propiedades para las figuras
        shape = random.choice(shapes)  # Tipo de figura
        color = random.choice(palette)  # Color
        size = random.randint(size_range[0], size_range[1])  # Tamaño
        active_shapes.append((shape, x, y, size, color))

    # Dibujar las figuras activas
    for shape, x, y, size, color in active_shapes:
        draw_shape(draw, shape, x, y, size, color)
"""


def generate_gif(output_file, width, height, frames, duration, background_color, palette, shapes, size_range, animation_type):
    """
    Genera un GIF procedural basado en las configuraciones del usuario.
    """
    # Diccionario de animaciones disponibles
    animations = {
        "Mosaico": generate_mosaic_animation,
        #"Burbujas": generate_bubbles_animation,
        #"Espiral": generate_spiral_animation,  # Nueva animación
    }

    if animation_type not in animations:
        console.print(f"[bold red]Animación '{animation_type}' no soportada. Usa una animación válida.[/bold red]")
        return

    images = []  # Lista para almacenar los frames del GIF
    for frame in range(frames):
        # Crear lienzo (fondo)
        if background_color:
            img = Image.new("RGB", (width, height), background_color)
        else:
            img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Generar un frame usando la animación seleccionada
        animations[animation_type](draw, frame, width, height, shapes, palette, size_range, frames)
        images.append(img)

    # Guardar el GIF
    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        duration=duration,  # Duración de cada frame
        loop=0  # Loop infinito
    )
    console.print(f"[bold green]GIF guardado como {output_file}[/bold green]")



# ======== Punto de entrada ========
if __name__ == "__main__":
    """
    # Obtener configuración del usuario
    background_color, shapes, palette = get_user_input()

    # Selección de animación
    console.print("\n🟪 Selecciona el [bold magenta]tipo de animación[/bold magenta]:")
    animation_type = Prompt.ask("   Opciones: [cyan]Mosaico[/cyan]", choices=["Mosaico"])
    """
    # Parámetros del GIF
    output_file = "output.gif"
    width, height = 500, 500  # Tamaño del lienzo
    frames = 30  # Número de frames
    # Pedir la duración a través de la consola
    duration = int(Prompt.ask("🕒 Ingresa la duración de cada frame en milisegundos (100 recomendado para velocidad normal)", default="100"))
    size_range = (20, 100)  # Tamaño mínimo y máximo de las figuras
 

    # Parámetros de ejemplo
    background_color = None
    shapes = ["rectangle"]
    palette = ["#12372A", "#436850", "#ADBC9F", "#FBFADA"]
    size_range = (10, 50)  # Tamaño de las figuras
    animation_type = "Mosaico"


    # Generar el GIF
    generate_gif(output_file, width, height, frames, duration, background_color, palette, shapes, size_range, animation_type)
