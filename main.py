from PIL import Image, ImageDraw
import random
import math
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()


def draw_shape(draw, shape, x, y, size, color):
    """
    Dibuja una figura específica en el canvas.
    """
    x1, y1 = x - size // 2, y - size // 2
    x2, y2 = x + size // 2, y + size // 2
    if shape == "circle":
        draw.ellipse([x1, y1, x2, y2], fill=color)
    elif shape == "rectangle":
        draw.rectangle([x1, y1, x2, y2], fill=color)
    elif shape == "triangle":
        draw.polygon([x1, y1, x2, y2, x, y - size], fill=color)


def generate_ordered_animation(draw, frame, width, height, shapes, palette, size_range, total_frames):
    """
    Genera el marco para la animación 'Ordenada'.
    """
    center_x, center_y = width // 2, height // 2
    spacing = max(size_range) + 10  # Espaciado entre figuras
    max_layers = total_frames // 2
    active_shapes = []

    # Crear figuras en capas concéntricas
    for layer in range(1, max_layers):
        num_figures = max(6, int(2 * math.pi * layer * spacing / max(size_range)))
        for i in range(num_figures):
            angle = (i / num_figures) * 2 * math.pi
            x = center_x + int(layer * spacing * math.cos(angle))
            y = center_y + int(layer * spacing * math.sin(angle))

            if layer <= frame:  # Agregar figura si está en rango del frame
                shape = random.choice(shapes)
                color = random.choice(palette)
                size = random.randint(size_range[0], size_range[1])
                active_shapes.append((shape, x, y, size, color))

    # Dibujar todas las figuras activas
    for shape, x, y, size, color in active_shapes:
        draw_shape(draw, shape, x, y, size, color)

    # Desaparición gradual
    if frame > total_frames // 2:
        disappear_frame = frame - (total_frames // 2)
        active_shapes = active_shapes[:-disappear_frame]


def generate_bubbles_animation(draw, frame, width, height, shapes, palette, size_range, total_frames):
    """
    Genera el marco para la animación 'Burbujas'.
    """
    active_shapes = []
    num_shapes = max(5, frame * 5 // total_frames)

    # Aparecer figuras aleatorias
    for _ in range(num_shapes):
        shape = random.choice(shapes)
        color = random.choice(palette)
        size = random.randint(size_range[0], size_range[1])
        x = random.randint(0, width)
        y = random.randint(0, height)
        active_shapes.append((shape, x, y, size, color))

    # Dibujar todas las figuras
    for shape, x, y, size, color in active_shapes:
        draw_shape(draw, shape, x, y, size, color)

    # Desaparición gradual
    if frame > total_frames // 2:
        disappear_frame = frame - (total_frames // 2)
        active_shapes = active_shapes[:-disappear_frame]


def generate_gif(output_file, width, height, frames, duration, background_color, palette, shapes, size_range, animation_type):
    """
    Genera un GIF procedural basado en las configuraciones del usuario.
    """
    animations = {
        "Ordenada": generate_ordered_animation,
        "Burbujas": generate_bubbles_animation,
    }

    if animation_type not in animations:
        console.print(f"[bold red]Animación '{animation_type}' no soportada. Usa una animación válida.[/bold red]")
        return

    images = []
    for frame in range(frames):
        if background_color:
            img = Image.new("RGB", (width, height), background_color)
        else:
            img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Llamar a la animación seleccionada
        animations[animation_type](draw, frame, width, height, shapes, palette, size_range, frames)
        images.append(img)

    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    console.print(f"[bold green]GIF guardado como {output_file}[/bold green]")


def validate_hex_color(color):
    """
    Valida si un color ingresado está en formato hexadecimal.
    """
    if len(color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in color):
        return True
    return False


def get_user_input():
    """
    Solicita los parámetros al usuario con una interfaz mejorada usando Rich.
    """
    # Descripción del procedimiento
    descripcion = """[bold green]🎨 [bold white]Bienvenido al[/bold white] Generador de GIFs Procedural![/bold green]
    
[bold green]Procedimiento para Generar un GIF Procedural:[/bold green] 

    1. [bold magenta]Escoger el fondo:[/bold magenta] El usuario deberá escoger el fondo, el cual puede o no tener un color. 
       Si se elige un fondo sin color, el GIF será transparente. 
    
    2. [bold magenta]Seleccionar las figuras:[/bold magenta] El usuario podrá agregar las figuras que desee dentro del GIF. 
       Las opciones disponibles son cuadrado, círculo y triángulo. 
    
    3. [bold magenta]Definir la paleta de colores:[/bold magenta] El usuario deberá ingresar los colores en formato hexadecimal. 
       Se recomienda visitar [link=https://colorhunt.co]colorhunt.co[/link] para ver referencias y elegir colores atractivos.
    
    4. [bold magenta]Seleccionar el tipo de animación:[/bold magenta] Por ejemplo, [cyan]Ordenada[/cyan] o [cyan]Burbujas[/cyan].

¡Sigue estos pasos para crear tu GIF personalizado y disfruta del proceso creativo!"""
    console.print(Panel(descripcion))

    # Fondo
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

    # Formas
    shapes = []
    console.print("\n🟪 Selecciona las [bold red]formas[/bold red] para incluir en el GIF:")
    if Prompt.ask("   ¿Círculos? 🔴", choices=["si", "no"]) == "si":
        shapes.append("circle")
    if Prompt.ask("   ¿Triángulos? 🔺", choices=["si", "no"]) == "si":
        shapes.append("triangle")
    if Prompt.ask("   ¿Cuadrados? 🟥", choices=["si", "no"]) == "si":
        shapes.append("rectangle")
    if not shapes:
        console.print("[bold yellow]No seleccionaste ninguna forma. Por defecto se usarán círculos.[/bold yellow]")
        shapes.append("circle")

    # Paleta de colores
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


if __name__ == "__main__":
    # Configuración inicial
    background_color, shapes, palette = get_user_input()

    # Elegir animación
    console.print("\n🟪 Selecciona el [green]tipo de animación[/green]:")
    animation_type = Prompt.ask("   Opciones: [green]Ordenada[/green], [green]Burbujas[/green]", choices=["Ordenada", "Burbujas"])

    output_file = "output.gif"
    width, height = 500, 500
    frames = 30
    duration = 100
    size_range = (20, 100)

    # Generar GIF
    generate_gif(output_file, width, height, frames, duration, background_color, palette, shapes, size_range, animation_type)
