
"""
Módulo: instrucciones
=====================
Contiene todas las funciones relacionadas con las instrucciones,
controles y elementos del juego “Ekeko y las Illas Sagradas”.

Este módulo está separado para mantener el código principal más limpio
y facilitar la generación de documentación automática mediante `pdoc`.

Autor: Grupo de Algoritmos y Estructura de Datos II
"""


# ================== IMPORTACIONES ==================
import pygame

# ================== CONSTANTES DE COLOR ==================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# ================== FUNCIONES ==================

def obtener_instrucciones():
    """
    Retorna las instrucciones generales del juego organizadas por secciones.

    Returns:
        list[str]: Lista de cadenas de texto que describen el objetivo,
                   controles, sistema de vidas, mochila y mecánicas del juego.
    """
    return [
        "🎯 OBJETIVO:",
        "Ayuda a Ekeko a recuperar las 19 Illas Sagradas robadas por los 14 Apus",
        "",
        "🕹️ CONTROLES:",
        "• A: Mover hacia la izquierda",
        "• D: Mover hacia la derecha", 
        "• W: Saltar",
        "• J: Ver/Ocultar mochila (inventario)",
        "• ↑↓: Navegar en preguntas",
        "• ENTER: Confirmar respuesta",
        "",
        "🎒 MOCHILA:",
        "• Presiona J para ver tu inventario",
        "• Las illas se muestran con sus GIFs animados",
        "• Contador de illas recolectadas",
        "• Layout organizado en grid 4x4",
        "",
        "❤️ SISTEMA DE VIDAS:",
        "• Tienes 3 corazones pixelados",
        "• Pierdes 1 vida por respuesta incorrecta",
        "• Sin vidas = Game Over",
        "",
        "🏔️ MECÁNICA DEL JUEGO:",
        "• Cada Apu te hará una pregunta sobre culturas peruanas",
        "• Respuesta correcta = Recibes illas + puerta se abre",
        "• Respuesta incorrecta = Pierdes vida + pregunta de nuevo",
        "• Completa las 14 escenas para ganar",
        "",
        "🚀 OPTIMIZACIONES:",
        "• Carga lazy de preguntas (solo cuando se necesitan)",
        "• Sistema de cache para mejor rendimiento",
        "• Archivos organizados en carpetas",
        "",
        "Presiona ESC o ENTER para volver al menú"
    ]


def obtener_controles_detallados():
    """
    Retorna un diccionario con los controles del juego clasificados por categoría.

    Returns:
        dict[str, dict[str, str]]: Controles de movimiento, interacción y juego.
    """
    return {
        "movimiento": {
            "A": "Mover hacia la izquierda",
            "D": "Mover hacia la derecha",
            "W": "Saltar"
        },
        "interaccion": {
            "J": "Ver/Ocultar mochila (inventario)",
            "↑↓": "Navegar en preguntas",
            "ENTER": "Confirmar respuesta",
            "ESC": "Volver al menú"
        },
        "juego": {
            "R": "Reiniciar juego (en Game Over)",
            "M": "Volver al menú (en Game Over)"
        }
    }


def obtener_informacion_mochila():
    """
    Retorna la configuración y detalles visuales de la mochila del juego.

    Returns:
        dict[str, str | int]: Información sobre dimensiones, posición y elementos visuales.
    """
    return {
        "tamaño": "300x400 píxeles",
        "posicion": "Centrada en pantalla",
        "fondo": "Semi-transparente",
        "illas_por_fila": 4,
        "max_filas": 4,
        "tamaño_illa": "40x40 píxeles",
        "animaciones": "GIFs animados de cada illa",
        "informacion": "Nombre de cada illa debajo de su GIF",
        "contador": "Illas Recolectadas: X/19"
    }


def obtener_informacion_apus():
    """
    Retorna una lista con los nombres y descripciones de los Apus del juego.

    Returns:
        list[str]: Nombres de las montañas o entidades espirituales del juego.
    """
    return [
        "Huascarán - Montaña Nevada",
        "Coropuna - Glaciar", 
        "Misti - Volcán",
        "Ampato - Altiplano",
        "Sara Sara - Volcán Andino",
        "Salkantay - Selva Alta",
        "Chachani - Desierto Alto",
        "Ccarhuarazo - Cordillera Central",
        "Rasuwillka - Montaña Sagrada",
        "Hualca Hualca - Volcán Nevado",
        "Uarancante - Pico Andino",
        "Allincapac - Montaña Dorada",
        "Katunqui - Volcán Inactivo",
        "Patallacta - Ruinas Sagradas"
    ]


def obtener_informacion_illas():
    """
    Retorna una lista con los nombres de las Illas Sagradas.

    Returns:
        list[str]: Nombres de los objetos sagrados recolectables.
    """
    return [
        "Tumi", "Chacana", "Illa", "Torito",
        "Perro Viringo", "Cuy", "Qullqi", "Quispe",
        "Qori", "Chuño", "Papa", "Maíz",
        "Calluha", "Cungalpo", "Hizanche",
        "Huashacara", "Inti", "Killa", "Chaska"
    ]


def dibujar_instrucciones(screen, font_title, font_text, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Dibuja las instrucciones del juego en la pantalla de Pygame.

    Args:
        screen (pygame.Surface): Superficie donde se dibujan los textos.
        font_title (pygame.font.Font): Fuente usada para el título.
        font_text (pygame.font.Font): Fuente usada para el texto.
        SCREEN_WIDTH (int): Ancho de la pantalla.
        SCREEN_HEIGHT (int): Alto de la pantalla.

    Nota:
        Si solo se va a documentar el código, no es necesario tener instalado `pygame`.
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    title_text = font_title.render("INSTRUCCIONES", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_text, title_rect)
    
    instructions = obtener_instrucciones()
    y_offset = 140
    
    for line in instructions:
        if line.startswith(("🎯", "🕹️", "❤️", "🏔️", "🎒", "🚀")):
            color = YELLOW
            font = pygame.font.SysFont("Arial", 20, bold=True)
        elif line.startswith("•"):
            color = WHITE
            font = font_text
        else:
            color = GREEN if line else WHITE
            font = font_text
        
        if line:
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text_surface, text_rect)
        
        y_offset += 25


if __name__ == "__main__":
    # Este bloque evita que el código se ejecute al importar el módulo
    # (por ejemplo, cuando se genera la documentación con pdoc)
    print("Módulo 'instrucciones' cargado correctamente. No se ejecuta código principal.")
