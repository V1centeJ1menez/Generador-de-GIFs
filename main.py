from PIL import Image, ImageDraw
import random
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.panel import Panel

console = Console()

def get_user_input():
    """
    Solicita los parámetros al usuario con una interfaz mejorada usando Rich.
    """
    # Descripción del procedimiento 
    descripcion = """[bold green]🎨 [bold white]Bienvenido al[/bold white] Generador de GIFs Procedural![/bold green]
    
[bold cyan]Procedimiento para Generar un GIF Procedural:[/bold cyan] 

    1. [bold]Escoger el fondo:[/bold] El usuario deberá escoger el fondo, el cual puede o no tener un color. 
       Si se elige un fondo sin color, el GIF será transparente. 
    
    2. [bold]Seleccionar las figuras:[/bold] El usuario podrá agregar las figuras que desee dentro del GIF. 
       Las opciones disponibles son cuadrado, círculo y triángulo. 
    
    3. [bold]Definir la paleta de colores:[/bold] El usuario deberá ingresar los colores en formato hexadecimal. 
       Se recomienda visitar [link=https://colorhunt.co]colorhunt.co[/link] para ver referencias y elegir colores atractivos.
    
    4. [bold]Definir el tipo de animación:[/bold] Proximamente.

¡Sigue estos pasos para crear tu GIF personalizado y disfruta del proceso creativo!""" 
    console.print(Panel(descripcion))


    # Fondo
    while True:
        background_choice = Prompt.ask(
            "¿Deseas un [bold white]color de fondo[/bold white] o un [bold white]fondo transparente[/bold white] (escribe [cyan]color[/cyan] o [yellow]sin fondo[/yellow])",
            choices=["color", "sin fondo"]
        )
        if background_choice == "color":
            background_color = Prompt.ask("Ingresa el [bold cyan]color de fondo[/bold cyan] en formato hexadecimal (ejemplo: FFFFFF)")
            if validate_hex_color(background_color):
                background_color = f"#{background_color}"
                break
            else:
                console.print("[bold red]El color ingresado no es válido. Intenta nuevamente.[/bold red]")
        else:
            background_color = None
            break

    # Formas
    shapes = []
    console.print("Selecciona las [bold cyan]formas[/bold cyan] para incluir en el GIF:")
    if Prompt.ask("¿Círculos?", choices=["si", "no"]) == "si":
        shapes.append("circle")
    if Prompt.ask("¿Triángulos?", choices=["si", "no"]) == "si":
        shapes.append("triangle")
    if Prompt.ask("¿Cuadrados?", choices=["si", "no"]) == "si":
        shapes.append("rectangle")
    if not shapes:
        console.print("[bold yellow]No seleccionaste ninguna forma. Por defecto se usarán círculos.[/bold yellow]")
        shapes.append("circle")

    # Paleta de colores
    palette = []
    console.print("Ingresa [bold cyan]4 colores[/bold cyan] para las figuras en formato hexadecimal:")
    for i in range(1, 5):
        while True:
            color = Prompt.ask(f"[cyan]Color {i}[/cyan]:")
            if validate_hex_color(color):
                palette.append(f"#{color}")
                break
            else:
                console.print("[bold red]El color ingresado no es válido. Intenta nuevamente.[/bold red]")

    return background_color, shapes, palette


def validate_hex_color(color):
    """
    Valida si un color ingresado está en formato hexadecimal.
    """
    if len(color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in color):
        return True
    return False


def generate_gif(output_file, width, height, frames, duration, background_color, palette, shapes, size_range):
    """
    Genera un GIF cíclico procedural basado en las configuraciones del usuario.
    """
    images = []

    for frame in range(frames):
        if background_color:
            img = Image.new("RGB", (width, height), background_color)
        else:
            img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for _ in range(random.randint(5, 15)):
            shape = random.choice(shapes)
            color = random.choice(palette)
            size = random.randint(size_range[0], size_range[1])
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2, y2 = x1 + size, y1 + size

            if shape == "circle":
                draw.ellipse([x1, y1, x2, y2], fill=color)
            elif shape == "rectangle":
                draw.rectangle([x1, y1, x2, y2], fill=color)
            elif shape == "triangle":
                draw.polygon([x1, y1, x2, y2, x1 + size // 2, y1 - size], fill=color)

        images.append(img)

    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    console.print(f"[bold green]GIF guardado como {output_file}[/bold green]")


if __name__ == "__main__":
    
    background_color, shapes, palette = get_user_input()

    output_file = "output.gif"
    width, height = 500, 500
    frames = 30
    duration = 100
    size_range = (20, 100)

    generate_gif(output_file, width, height, frames, duration, background_color, palette, shapes, size_range)
