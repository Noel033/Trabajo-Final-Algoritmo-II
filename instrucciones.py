# ================== INSTRUCCIONES DEL JUEGO ==================
# Archivo separado con todas las instrucciones del juego
# Para mantener el código principal más limpio y organizado

import pygame

# Colores para las instrucciones (estilo libro de brujas)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BROWN = (101, 67, 33)
DARK_BROWN = (61, 40, 18)
CREAM = (255, 248, 220)
GOLD = (255, 215, 0)

def obtener_instrucciones_pagina1():
    """Retorna las instrucciones de la primera página"""
    return [
        ("OBJETIVO", "SECCIÓN", True),
        ("Ayuda a Ekeko a recuperar las 19", "TEXTO", False),
        ("Illas Sagradas robadas por los 14 Apus", "TEXTO", False),
        ("", "ESPACIO", False),
        ("CONTROLES", "SECCIÓN", True),
        ("A - Mover hacia la izquierda", "CONTROL", False),
        ("D - Mover hacia la derecha", "CONTROL", False),
        ("W - Saltar", "CONTROL", False),
        ("J - Ver/Ocultar mochila", "CONTROL", False),
        ("↑↓ - Navegar en preguntas", "CONTROL", False),
        ("ENTER - Confirmar respuesta", "CONTROL", False),
        ("ESC - Volver al menú", "CONTROL", False),
        ("", "ESPACIO", False),
        ("MOCHILA", "SECCIÓN", True),
        ("Presiona J para ver tu inventario", "TEXTO", False),
        ("Las illas se muestran con sus GIFs", "TEXTO", False),
        ("Contador de illas recolectadas", "TEXTO", False),
        ("Layout organizado en grid", "TEXTO", False),
    ]

def obtener_instrucciones_pagina2():
    """Retorna las instrucciones de la segunda página"""
    return [
        ("SISTEMA DE VIDAS", "SECCIÓN", True),
        ("Tienes 3 corazones pixelados", "TEXTO", False),
        ("Pierdes 1 vida por respuesta", "TEXTO", False),
        ("incorrecta", "TEXTO", False),
        ("Sin vidas = Game Over", "TEXTO", False),
        ("", "ESPACIO", False),
        ("MECÁNICA DEL JUEGO", "SECCIÓN", True),
        ("Cada Apu te hará una pregunta", "TEXTO", False),
        ("sobre culturas peruanas", "TEXTO", False),
        ("", "ESPACIO", False),
        ("Respuesta correcta:", "TEXTO", False),
        ("✓ Recibes illas sagradas", "TEXTO", False),
        ("✓ Portal se abre", "TEXTO", False),
        ("✓ Puedes avanzar", "TEXTO", False),
        ("", "ESPACIO", False),
        ("Respuesta incorrecta:", "TEXTO", False),
        ("✗ Pierdes una vida", "TEXTO", False),
        ("✗ Debes intentar de nuevo", "TEXTO", False),
        ("", "ESPACIO", False),
        ("Completa las 14 escenas", "TEXTO", False),
        ("para ganar el juego", "TEXTO", False),
    ]

def dibujar_pagina_libro(screen, book_surface, book_width, book_height, instructions, page_num, total_pages):
    """Dibuja una página del libro con las instrucciones"""
    
    section_font = pygame.font.SysFont("Arial", 16, bold=True)
    text_font = pygame.font.SysFont("Arial", 13)
    control_font = pygame.font.SysFont("Arial", 12)
    
    y_offset = 70
    line_height = 18
    
    for instruction, tipo, is_section in instructions:
        if tipo == "ESPACIO":
            y_offset += line_height // 2
            continue
        
        x_pos = 50
        if tipo == "SECCIÓN":
            # Título de sección con decoración
            pygame.draw.line(book_surface, GOLD, (x_pos - 8, y_offset), (x_pos - 12, y_offset), 2)
            text_surface = section_font.render(instruction, True, DARK_BROWN)
            book_surface.blit(text_surface, (x_pos, y_offset - 2))
            pygame.draw.line(book_surface, GOLD, 
                           (x_pos + text_surface.get_width() + 5, y_offset),
                           (book_width - x_pos, y_offset), 2)
            y_offset += line_height + 4
        elif tipo == "CONTROL":
            # Controles con viñeta
            pygame.draw.circle(book_surface, GOLD, (x_pos - 6, y_offset + 5), 2)
            text_surface = control_font.render(instruction, True, BLACK)
            book_surface.blit(text_surface, (x_pos, y_offset))
            y_offset += line_height
        else:  # TEXTO normal
            text_surface = text_font.render(instruction, True, BLACK)
            book_surface.blit(text_surface, (x_pos, y_offset))
            y_offset += line_height
    
    # Número de página
    page_font = pygame.font.SysFont("Arial", 10, italic=True)
    page_text = page_font.render(f"Página {page_num} de {total_pages}", True, BROWN)
    page_rect = page_text.get_rect(center=(book_width // 2, book_height - 20))
    book_surface.blit(page_text, page_rect)

def dibujar_instrucciones(screen, font_title, font_text, SCREEN_WIDTH, SCREEN_HEIGHT):
    """Función para dibujar las instrucciones en pantalla con estilo libro de brujas (2 páginas)"""
    
    # Variable estática para la página actual
    if not hasattr(dibujar_instrucciones, 'pagina_actual'):
        dibujar_instrucciones.pagina_actual = 1
    
    # Fondo con textura de pergamino
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(230)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Crear superficie para el libro (dos páginas)
    book_width = (SCREEN_WIDTH - 120) // 2  # Ancho de cada página
    book_height = SCREEN_HEIGHT - 100
    book_x_left = (SCREEN_WIDTH - (book_width * 2 + 20)) // 2
    book_y = (SCREEN_HEIGHT - book_height) // 2
    
    # Página izquierda (siempre visible)
    page1_surface = pygame.Surface((book_width, book_height))
    page1_surface.fill(CREAM)
    pygame.draw.rect(page1_surface, DARK_BROWN, (0, 0, book_width, book_height), 6)
    
    # Título en página izquierda
    title_font = pygame.font.SysFont("Arial", 20, bold=True)
    title_text = title_font.render("LIBRO DE LAS", True, DARK_BROWN)
    title_rect = title_text.get_rect(center=(book_width // 2, 20))
    page1_surface.blit(title_text, title_rect)
    subtitle_text = title_font.render("ARTES SAGRADAS", True, DARK_BROWN)
    subtitle_rect = subtitle_text.get_rect(center=(book_width // 2, 40))
    page1_surface.blit(subtitle_text, subtitle_rect)
    
    # Línea decorativa
    pygame.draw.line(page1_surface, GOLD, (30, 50), (book_width - 30, 50), 2)
    
    # Dibujar contenido de página 1
    instrucciones_p1 = obtener_instrucciones_pagina1()
    dibujar_pagina_libro(screen, page1_surface, book_width, book_height, instrucciones_p1, 1, 2)
    
    # Página derecha
    page2_surface = pygame.Surface((book_width, book_height))
    page2_surface.fill(CREAM)
    pygame.draw.rect(page2_surface, DARK_BROWN, (0, 0, book_width, book_height), 6)
    
    # Línea decorativa superior en página derecha
    pygame.draw.line(page2_surface, GOLD, (30, 30), (book_width - 30, 30), 2)
    
    # Dibujar contenido de página 2
    instrucciones_p2 = obtener_instrucciones_pagina2()
    dibujar_pagina_libro(screen, page2_surface, book_width, book_height, instrucciones_p2, 2, 2)
    
    # Sombra del libro
    shadow_surface = pygame.Surface((book_width * 2 + 30, book_height + 10))
    shadow_surface.set_alpha(100)
    shadow_surface.fill(BLACK)
    screen.blit(shadow_surface, (book_x_left - 5, book_y - 5))
    
    # Dibujar ambas páginas
    screen.blit(page1_surface, (book_x_left, book_y))
    screen.blit(page2_surface, (book_x_left + book_width + 20, book_y))
    
    # Línea central (lomo del libro)
    pygame.draw.line(screen, DARK_BROWN, 
                    (book_x_left + book_width + 10, book_y),
                    (book_x_left + book_width + 10, book_y + book_height), 4)
    
    # Decoración de estrellas mágicas alrededor
    import math
    for i in range(10):
        angle = (360 / 10) * i
        dist = 130
        star_x = SCREEN_WIDTH // 2 + int(dist * math.cos(math.radians(angle)))
        star_y = SCREEN_HEIGHT // 2 + int(dist * math.sin(math.radians(angle)))
        star_size = 2
        pygame.draw.circle(screen, GOLD, (star_x, star_y), star_size)
        pygame.draw.line(screen, GOLD, (star_x - star_size, star_y), (star_x + star_size, star_y), 1)
        pygame.draw.line(screen, GOLD, (star_x, star_y - star_size), (star_x, star_y + star_size), 1)
    
    # Instrucciones de navegación
    nav_font = pygame.font.SysFont("Arial", 12, italic=True)
    nav_text = nav_font.render("Presiona ESC o ENTER para cerrar el libro", True, BROWN)
    nav_rect = nav_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    screen.blit(nav_text, nav_rect)
