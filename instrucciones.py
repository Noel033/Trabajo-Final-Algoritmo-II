# ================== INSTRUCCIONES DEL JUEGO ==================
# Archivo separado con todas las instrucciones del juego
# Para mantener el código principal más limpio y organizado

import pygame

# Colores para las instrucciones
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

def obtener_instrucciones():
    """Retorna las instrucciones del juego organizadas por secciones"""
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
    """Retorna información detallada sobre los controles"""
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
    """Retorna información detallada sobre la mochila"""
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
    """Retorna información sobre los Apus del juego"""
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
    """Retorna información sobre las illas sagradas"""
    return [
        "Tumi", "Chacana", "Illa", "Torito",
        "Perro Viringo", "Cuy", "Qullqi", "Quispe",
        "Qori", "Chuño", "Papa", "Maíz",
        "Calluha", "Cungalpo", "Hizanche",
        "Huashacara", "Inti", "Killa", "Chaska"
    ]

def dibujar_instrucciones(screen, font_title, font_text, SCREEN_WIDTH, SCREEN_HEIGHT):
    """Función para dibujar las instrucciones en pantalla"""
    # Fondo semi-transparente
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Título
    title_text = font_title.render("INSTRUCCIONES", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_text, title_rect)
    
    # Instrucciones
    instructions = obtener_instrucciones()
    y_offset = 140
    
    for line in instructions:
        if line.startswith("🎯") or line.startswith("🕹️") or line.startswith("❤️") or line.startswith("🏔️") or line.startswith("🎒") or line.startswith("🚀"):
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
