import pygame
import sys
import os
import random
import math
from PIL import Image

# ================== PYGAME INICIO ==================
pygame.init()
pygame.mixer.init()  # Inicializar el mixer para sonido

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("La Travesía de Ekeko - 12 Escenas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# FPS
FPS = 60
clock = pygame.time.Clock()

# ================== DATOS DEL JUEGO ==================
APUS_DATA = {
    "Huascarán": {"color": (255, 255, 255), "health": 100, "bioma": "Montaña Nevada", "gif": "coropuna.gif"},
    "Misti": {"color": (255, 150, 150), "health": 85, "bioma": "Volcán", "gif": "coropuna.gif"},
    "Coropuna": {"color": (200, 200, 255), "health": 90, "bioma": "Glaciar", "gif": "coropuna.gif"},
    "Ampato": {"color": (150, 255, 150), "health": 95, "bioma": "Altiplano", "gif": "ampato.gif"},
    "Chachani": {"color": (255, 200, 100), "health": 80, "bioma": "Desierto Alto", "gif": "coropuna.gif"},
    "Sabancaya": {"color": (255, 100, 100), "health": 88, "bioma": "Volcán Activo", "gif": "coropuna.gif"},
    "Alpamayo": {"color": (200, 255, 255), "health": 92, "bioma": "Pico Nevado", "gif": "coropuna.gif"},
    "Yerupajá": {"color": (180, 180, 255), "health": 98, "bioma": "Cordillera", "gif": "coropuna.gif"},
    "Ausangate": {"color": (255, 180, 255), "health": 85, "bioma": "Laguna Sagrada", "gif": "coropuna.gif"},
    "Salkantay": {"color": (100, 255, 200), "health": 90, "bioma": "Selva Alta", "gif": "coropuna.gif"},
    "Chopicalqui": {"color": (255, 255, 150), "health": 87, "bioma": "Valle Glaciar", "gif": "coropuna.gif"},
    "Cotopaxi": {"color": (200, 100, 255), "health": 100, "bioma": "Cima Suprema", "gif": "coropuna.gif"}
}

# GIFs de fondo para cada escena/bioma
BIOMA_GIFS = [
    "primerBio.gif",                 # Huascarán - AQUÍ PUEDES CAMBIAR POR TU GIF
    "segundoBio.gif",                  # Misti - AQUÍ PUEDES CAMBIAR POR TU GIF
    "bioma3_glaciar.gif",             # Coropuna
    "bioma4_altiplano.gif",           # Ampato
    "bioma5_desierto_alto.gif",       # Chachani
    "bioma6_volcan_activo.gif",       # Sabancaya
    "bioma7_pico_nevado.gif",         # Alpamayo
    "bioma8_cordillera.gif",          # Yerupajá
    "bioma9_laguna_sagrada.gif",      # Ausangate
    "bioma10_selva_alta.gif",         # Salkantay
    "bioma11_valle_glaciar.gif",      # Chopicalqui
    "bioma12_cima_suprema.gif"        # Cotopaxi
]

# Música para cada bioma (puedes agregar archivos .mp3 o .ogg)
BIOMA_MUSIC = [
    "musica1.mp3",          # Huascarán - AQUÍ PONES TU MÚSICA
    "musica_2.mp3",              # Misti - AQUÍ PONES TU MÚSICA
    "musica3_coropuna.mp3",           # Coropuna
    "musica4_ampato.mp3",             # Ampato
    "musica5_chachani.mp3",           # Chachani
    "musica6_sabancaya.mp3",          # Sabancaya
    "musica7_alpamayo.mp3",           # Alpamayo
    "musica8_yerupaja.mp3",           # Yerupajá
    "musica9_ausangate.mp3",          # Ausangate
    "musica10_salkantay.mp3",         # Salkantay
    "musica11_chopicalqui.mp3",       # Chopicalqui
    "musica12_cotopaxi.mp3"           # Cotopaxi
]

# Illas robadas divididas entre los 12 Apus (19 artículos total)
ILLAS_ROBADAS_POR_ESCENA = [
    # Escena 1 - Huascarán (2 illas)
    ["Tumi", "Chacana"],
    # Escena 2 - Misti (2 illas)  
    ["Illa", "Torito"],
    # Escena 3 - Coropuna (2 illas)
    ["Perro Viringo", "Cuy"],
    # Escena 4 - Ampato (2 illas)
    ["Qullqi", "Quispe"],
    # Escena 5 - Chachani (2 illas)
    ["Qori", "Chuño"],
    # Escena 6 - Sabancaya (2 illas)
    ["Papa", "Maíz"],
    # Escena 7 - Alpamayo (1 illa)
    ["Calluha"],
    # Escena 8 - Yerupajá (1 illa)
    ["Cungalpo"],
    # Escena 9 - Ausangate (1 illa)
    ["Hizanche"],
    # Escena 10 - Salkantay (1 illa)
    ["Huashacara"],
    # Escena 11 - Chopicalqui (1 illa)
    ["Inti"],
    # Escena 12 - Cotopaxi (2 illas restantes)
    ["Killa", "Chaska"]
]

# GIFs para cada illa robada
ILLAS_GIFS = {
    "Tumi": "tumi.gif",
    "Chacana": "chacana.gif", 
    "Illa": "illa.gif",
    "Torito": "torito.gif",
    "Perro Viringo": "perro_viringo.gif",
    "Cuy": "cuy.gif",
    "Qullqi": "qullqi.gif",
    "Quispe": "quispe.gif",
    "Qori": "qori.gif",
    "Chuño": "chuno.gif",
    "Papa": "papa.gif",
    "Maíz": "maiz.gif",
    "Calluha": "calluha.gif",
    "Cungalpo": "cungalpo.gif",
    "Hizanche": "hizanche.gif",
    "Huashacara": "huashacara.gif",
    "Inti": "inti.gif",
    "Killa": "killa.gif",
    "Chaska": "chaska.gif"
}

# Preguntas para cada Apu
PREGUNTAS_APUS = [
    {
        "apu": "Huascarán",
        "pregunta": "¿Qué civilización es conocida por sus impresionantes líneas trazadas en el desierto que solo pueden verse desde el aire?",
        "opciones": ["Mochica", "Nazca", "Chavín", "Wari"],
        "respuesta_correcta": 1
    },
    {
        "apu": "Misti",
        "pregunta": "¿Cuál fue la capital del Imperio Inca?",
        "opciones": ["Cusco", "Machu Picchu", "Ollantaytambo", "Sacsayhuamán"],
        "respuesta_correcta": 0
    },
    {
        "apu": "Coropuna",
        "pregunta": "¿Qué cultura es famosa por sus huacos retratos y su avanzada metalurgia?",
        "opciones": ["Nazca", "Chavín", "Mochica", "Chimú"],
        "respuesta_correcta": 2
    },
    {
        "apu": "Ampato",
        "pregunta": "¿Cuál es el nombre del sistema de nudos usado por los incas para registrar información?",
        "opciones": ["Quipu", "Tocapu", "Ayllu", "Mit'a"],
        "respuesta_correcta": 0
    },
    {
        "apu": "Chachani",
        "pregunta": "¿Qué cultura construyó el famoso templo de Chavín de Huántar?",
        "opciones": ["Wari", "Tiahuanaco", "Chavín", "Paracas"],
        "respuesta_correcta": 2
    },
    {
        "apu": "Sabancaya",
        "pregunta": "¿Cómo se llamaba el emperador inca cuando llegaron los españoles?",
        "opciones": ["Huáscar", "Atahualpa", "Manco Inca", "Túpac Amaru"],
        "respuesta_correcta": 1
    },
    {
        "apu": "Alpamayo",
        "pregunta": "¿Qué cultura creó los famosos mantos de Paracas?",
        "opciones": ["Paracas", "Nazca", "Ica", "Chincha"],
        "respuesta_correcta": 0
    },
    {
        "apu": "Yerupajá",
        "pregunta": "¿Cuál era la moneda de intercambio principal en el Imperio Inca?",
        "opciones": ["Oro", "Plata", "No usaban moneda", "Cobre"],
        "respuesta_correcta": 2
    },
    {
        "apu": "Ausangate",
        "pregunta": "¿Qué significa 'Tahuantinsuyu'?",
        "opciones": ["Casa del Sol", "Cuatro regiones", "Gran Imperio", "Tierra Sagrada"],
        "respuesta_correcta": 1
    },
    {
        "apu": "Salkantay",
        "pregunta": "¿Qué cultura desarrolló la técnica agrícola de andenes o terrazas?",
        "opciones": ["Nazca", "Inca", "Wari", "Todas las anteriores"],
        "respuesta_correcta": 3
    },
    {
        "apu": "Chopicalqui",
        "pregunta": "¿Cómo se llamaba el dios principal de los incas?",
        "opciones": ["Viracocha", "Inti", "Mama Quilla", "Pachacamac"],
        "respuesta_correcta": 1
    },
    {
        "apu": "Cotopaxi",
        "pregunta": "¿Cuál fue la primera capital de los incas antes de Cusco?",
        "opciones": ["Paqariq Tampu", "Ollantaytambo", "Pisaq", "Machu Picchu"],
        "respuesta_correcta": 0
    }
]

# ================== FUNCIONES ==================
def load_gif_frames(gif_path):
    """Carga todos los frames de un GIF como superficies pygame"""
    try:
        gif = Image.open(gif_path)
        frames = []
        for frame_num in range(gif.n_frames):
            gif.seek(frame_num)
            frame = gif.copy()
            if frame.mode != "RGBA":
                frame = frame.convert("RGBA")
            frame_surface = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            frames.append(frame_surface)
        return frames
    except Exception as e:
        print(f"Error cargando GIF {gif_path}: {e}")
        return None

def load_music(music_path):
    """Carga música de fondo"""
    try:
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            return True
        return False
    except Exception as e:
        print(f"Error cargando música {music_path}: {e}")
        return False

def play_music(music_path, loop=-1):
    """Reproduce música de fondo"""
    try:
        if load_music(music_path):
            pygame.mixer.music.play(loop)  # -1 = loop infinito
            return True
        return False
    except Exception as e:
        print(f"Error reproduciendo música: {e}")
        return False

def stop_music():
    """Detiene la música de fondo"""
    pygame.mixer.music.stop()

def draw_pixelated_hearts(screen, lives, max_lives, x, y):
    """Dibuja corazones pixelados estilo Minecraft"""
    heart_size = 20
    spacing = 25
    
    for i in range(max_lives):
        heart_x = x + (i * spacing)
        heart_y = y
        
        if i >= lives:
            color = GRAY
        else:
            color = RED
        
        # Dibujar corazón pixelado
        pygame.draw.rect(screen, color, (heart_x + 4, heart_y + 2, 4, 4))
        pygame.draw.rect(screen, color, (heart_x + 12, heart_y + 2, 4, 4))
        pygame.draw.rect(screen, color, (heart_x + 2, heart_y + 6, 16, 4))
        pygame.draw.rect(screen, color, (heart_x + 4, heart_y + 10, 12, 4))
        pygame.draw.rect(screen, color, (heart_x + 6, heart_y + 14, 8, 4))
        pygame.draw.rect(screen, color, (heart_x + 8, heart_y + 18, 4, 4))
        
# ================== MENÚ PRINCIPAL ==================
class MainMenu:
    def __init__(self):
        self.selected_option = 0
        self.options = ["JUGAR", "INSTRUCCIONES", "SALIR"]
        self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_options = pygame.font.SysFont("Arial", 32, bold=True)
        
        # Cargar fondo del menú - AQUÍ PONES TU IMAGEN DE FONDO
        self.background_frames = None
        menu_bg_path = "menu_background.gif"  # CAMBIA ESTE NOMBRE POR TU GIF DE FONDO
        if os.path.exists(menu_bg_path):
            self.background_frames = load_gif_frames(menu_bg_path)
            if self.background_frames:
                self.background_frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in self.background_frames]
                self.current_frame = 0
                self.animation_timer = 0
                self.animation_speed = 0.1
        
        # Si no hay GIF, crear fondo estático
        if not self.background_frames:
            self.create_static_background()
        
        # Cargar y reproducir música del menú - AQUÍ PONES TU MÚSICA
        self.menu_music_path = "menu_music.mp3"  # CAMBIA ESTE NOMBRE POR TU MÚSICA
        if os.path.exists(self.menu_music_path):
            play_music(self.menu_music_path)
            print(f"🎵 Reproduciendo música del menú: {self.menu_music_path}")
        else:
            print("🎵 Archivo de música del menú no encontrado")

    def create_static_background(self):
        """Crear fondo estático si no hay GIF"""
        self.static_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Degradado de cielo
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(250 + (255 - 250) * color_ratio)
            pygame.draw.line(self.static_background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Suelo verde
        pygame.draw.rect(self.static_background, (34, 139, 34), (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

    def update(self):
        if self.background_frames:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.background_frames)

    def draw(self, screen):
        # Dibujar fondo
        if self.background_frames:
            screen.blit(self.background_frames[self.current_frame], (0, 0))
        else:
            screen.blit(self.static_background, (0, 0))
        
        # Título principal
        title_text = self.font_title.render("LA TRAVESÍA DE EKEKO", True, WHITE)
        title_shadow = self.font_title.render("LA TRAVESÍA DE EKEKO", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 150 + 3))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.font_subtitle.render("Rescata las 19 Illas Sagradas de los 12 Apus", True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú
        start_y = 300
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            shadow_color = BLACK
            
            text_surface = self.font_options.render(option, True, color)
            shadow_surface = self.font_options.render(option, True, shadow_color)
            
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 60))
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 2, start_y + i * 60 + 2))
            
            screen.blit(shadow_surface, shadow_rect)
            screen.blit(text_surface, text_rect)
        
        # Instrucciones de navegación
        nav_text = pygame.font.SysFont("Arial", 16).render("Usa ↑↓ para navegar, ENTER para seleccionar", True, WHITE)
        nav_rect = nav_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(nav_text, nav_rect)


# ================== PANTALLA DE INSTRUCCIONES ==================
class InstructionsScreen:
    def __init__(self):
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 18)
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "BACK"
        return None
    
    def draw(self, screen):
        # Fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Título
        title_text = self.font_title.render("INSTRUCCIONES", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Instrucciones
        instructions = [
            "🎯 OBJETIVO:",
            "Ayuda a Ekeko a recuperar las 19 Illas Sagradas robadas por los 12 Apus",
            "",
            "🕹️ CONTROLES:",
            "• Flechas ← → o A/D: Mover",
            "• Espacio o ↑: Saltar",
            "• ↑↓: Navegar en preguntas",
            "• ENTER: Confirmar respuesta",
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
            "• Completa las 12 escenas para ganar",
            "",
            "Presiona ESC o ENTER para volver al menú"
        ]
        
        y_offset = 140
        for line in instructions:
            if line.startswith("🎯") or line.startswith("🕹️") or line.startswith("❤️") or line.startswith("🏔️"):
                color = YELLOW
                font = pygame.font.SysFont("Arial", 20, bold=True)
            elif line.startswith("•"):
                color = WHITE
                font = self.font_text
            else:
                color = GREEN if line else WHITE
                font = self.font_text
            
            if line:
                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text_surface, text_rect)
            
            y_offset += 25


# ================== CLASES DEL JUEGO ==================
class Player:
    def __init__(self, x, y, gif_path=None, scale_factor=1.0):
        self.scale_factor = scale_factor
        if gif_path and os.path.exists(gif_path):
            self.frames = load_gif_frames(gif_path)
            if self.frames:
                self.frames = [pygame.transform.scale(f, (int(f.get_width()*scale_factor),
                                                          int(f.get_height()*scale_factor))) for f in self.frames]
                self.image = self.frames[0]
                self.original_frames = self.frames[:]
            else:
                self.create_placeholder()
        else:
            self.create_placeholder()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.8
        self.jump_strength = -15
        self.facing_right = True
        self.walking = False
        self.frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        
        # Sistema de vidas
        self.lives = 3
        self.max_lives = 3
        
        self.articulos_collected = []
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def create_placeholder(self):
        self.frames = []
        width = int(40 * self.scale_factor)
        height = int(60 * self.scale_factor)
        colors = [(255, 100, 100), (100, 255, 100), (150, 100, 255), (255, 150, 100)]
        for c in colors:
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.fill(c)
            self.frames.append(frame)
        self.image = self.frames[0]
        self.original_frames = self.frames[:]

    def update(self):
        if not self.on_ground:
            self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        ground_level = SCREEN_HEIGHT - 150
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        self.update_animation()

    def update_animation(self):
        if self.walking or not self.on_ground:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.original_frames[self.frame_index], True, False)
                else:
                    self.image = self.original_frames[self.frame_index]
        else:
            self.image = self.original_frames[0]

    def handle_input(self, keys):
        self.vel_x = 0
        self.walking = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
            self.walking = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
            self.walking = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            return self.lives > 0
        return False

    def collect_articulos(self, articulos_list):
        for articulo in articulos_list:
            if articulo not in self.articulos_collected:
                self.articulos_collected.append(articulo)
                print(f"🎒 Ekeko recolectó: {articulo}")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text_surface = self.font.render("Ekeko", True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(text_surface, text_rect)


class Apu:
    def __init__(self, name, x, y, scene_number=0):
        self.name = name
        self.data = APUS_DATA[name]
        self.size = 80
        self.health = self.data["health"]
        self.max_health = self.data["health"]
        self.scene_number = scene_number

        apu_gif_path = self.data["gif"]
        self.frames = None
        if apu_gif_path and os.path.exists(apu_gif_path):
            self.frames = load_gif_frames(apu_gif_path)
        if self.frames:
            self.frames = [pygame.transform.scale(f, (self.size, self.size)) for f in self.frames]
            self.image = self.frames[0]
            self.original_frames = self.frames[:]
        else:
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(self.data["color"])
            self.original_frames = [self.image]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def update(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.original_frames)
            self.image = self.original_frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text_surface = self.font.render(f"Apu {self.name}", True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(text_surface, text_rect)

    def give_illas_to_player(self, player, scene_number):
        """El Apu entrega las illas robadas al Ekeko"""
        illas = ILLAS_ROBADAS_POR_ESCENA[scene_number]
        message = f"🎁 Apu {self.name} te entrega las illas sagradas: "
        
        for illa in illas:
            player.collect_articulos([illa])
            message += f"{illa}, "
        
        message = message.rstrip(", ") + " ¡Guárdalas en tu bolsillo!"
        print(message)
        return illas


class Door:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 100)
        self.is_open = False
        self.opening_animation = 0
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def open_door(self):
        self.is_open = True

    def update(self):
        if self.is_open and self.opening_animation < 1:
            self.opening_animation += 0.05

    def draw(self, screen):
        if not self.is_open:
            pygame.draw.rect(screen, (101, 67, 33), self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 3)
            pygame.draw.circle(screen, YELLOW, (self.rect.right - 15, self.rect.centery), 3)
        else:
            open_width = int(self.rect.width * (1 - self.opening_animation))
            if open_width > 0:
                open_rect = pygame.Rect(self.rect.x, self.rect.y, open_width, self.rect.height)
                pygame.draw.rect(screen, (101, 67, 33), open_rect)
                pygame.draw.rect(screen, BLACK, open_rect, 3)
            
            if self.opening_animation > 0.5:
                text_surface = self.font.render("¡Puerta Abierta!", True, GREEN)
                text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
                screen.blit(text_surface, text_rect)


class Articulo:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 30, 30)
        self.collected = False
        self.color = (255, 255, 0)
        self.float_timer = 0
        self.base_y = y
        self.font = pygame.font.SysFont("Arial", 12, bold=True)
        
        self.frames = None
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        if name in ILLAS_GIFS:
            gif_path = ILLAS_GIFS[name]
            if os.path.exists(gif_path):
                self.frames = load_gif_frames(gif_path)
                if self.frames:
                    self.frames = [pygame.transform.scale(f, (25, 25)) for f in self.frames]

    def update(self):
        if not self.collected:
            self.float_timer += 0.1
            self.rect.y = self.base_y + int(5 * math.cos(self.float_timer))
            
            if self.frames:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        if not self.collected:
            if self.frames:
                frame_rect = self.frames[self.current_frame].get_rect(center=self.rect.center)
                screen.blit(self.frames[self.current_frame], frame_rect)
            else:
                pygame.draw.circle(screen, self.color, self.rect.center, 12)
                pygame.draw.circle(screen, WHITE, self.rect.center, 12, 2)
            
            text_surface = self.font.render(self.name, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 12))
            screen.blit(text_surface, text_rect)
            
# ================== PARTE 3 - GAME MANAGER Y SISTEMA PRINCIPAL ==================

class QuestionScreen:
    def __init__(self, pregunta_data):
        self.pregunta_data = pregunta_data
        self.font_title = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_question = pygame.font.SysFont("Arial", 18)
        self.font_options = pygame.font.SysFont("Arial", 16)
        self.selected_option = 0
        self.answered = False
        self.correct = False
        self.show_result = False
        self.result_timer = 0

    def handle_input(self, event):
        if not self.answered:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.selected_option > 0:
                    self.selected_option -= 1
                elif event.key == pygame.K_DOWN and self.selected_option < len(self.pregunta_data["opciones"]) - 1:
                    self.selected_option += 1
                elif event.key == pygame.K_RETURN:
                    self.answered = True
                    self.correct = (self.selected_option == self.pregunta_data["respuesta_correcta"])
                    self.show_result = True
                    self.result_timer = 120

    def update(self):
        if self.show_result and self.result_timer > 0:
            self.result_timer -= 1

    def draw(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        apu_text = self.font_title.render(f"Apu {self.pregunta_data['apu']} te pregunta:", True, WHITE)
        apu_rect = apu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(apu_text, apu_rect)

        question_lines = self.wrap_text(self.pregunta_data["pregunta"], self.font_question, SCREEN_WIDTH - 100)
        y_offset = 150
        for line in question_lines:
            text_surface = self.font_question.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 25

        if not self.show_result:
            y_offset += 30
            for i, opcion in enumerate(self.pregunta_data["opciones"]):
                color = YELLOW if i == self.selected_option else WHITE
                option_text = f"{chr(65 + i)}) {opcion}"
                text_surface = self.font_options.render(option_text, True, color)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text_surface, text_rect)
                y_offset += 30

            instr_text = self.font_options.render("Usa ↑↓ para seleccionar, ENTER para confirmar", True, GRAY)
            instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(instr_text, instr_rect)

        if self.show_result:
            if self.correct:
                result_text = "¡CORRECTO! El Apu te permite pasar"
                color = GREEN
            else:
                result_text = "¡INCORRECTO! Pierdes una vida"
                color = RED
            
            text_surface = self.font_title.render(result_text, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)

            if self.correct:
                correct_answer = self.pregunta_data["opciones"][self.pregunta_data["respuesta_correcta"]]
                answer_text = f"Respuesta: {correct_answer}"
                answer_surface = self.font_question.render(answer_text, True, WHITE)
                answer_rect = answer_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
                screen.blit(answer_surface, answer_rect)

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def is_finished(self):
        return self.show_result and self.result_timer <= 0


class GameScene:
    def __init__(self, scene_number):
        self.scene_number = scene_number
        self.apu_name = list(APUS_DATA.keys())[scene_number]
        self.apu = Apu(self.apu_name, SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 230, scene_number)
        self.door = Door(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 250)
        self.question_screen = None
        self.completed = False
        self.showing_question = False
        self.player_can_advance = False
        self.illas_message = ""
        self.illas_message_timer = 0
        
        # Crear artículos visibles que flotan en la escena
        self.artikulos_visuales = []
        self.create_visual_artikulos()

    def create_visual_artikulos(self):
        """Crear artículos visuales que aparecerán después de responder correctamente"""
        illas_de_esta_escena = ILLAS_ROBADAS_POR_ESCENA[self.scene_number]
        x_start = 150
        spacing = 100
        
        for i, illa_name in enumerate(illas_de_esta_escena):
            x = x_start + (i * spacing)
            y = SCREEN_HEIGHT - 250
            articulo = Articulo(illa_name, x, y)
            articulo.collected = True  # Empiezan como "recolectados" (invisibles)
            self.artikulos_visuales.append(articulo)

    def show_artikulos(self):
        """Hacer visibles los artículos cuando el Apu los entrega"""
        for articulo in self.artikulos_visuales:
            articulo.collected = False  # Hacerlos visibles
        
        # Timer para recolectarlos automáticamente después de un tiempo
        self.auto_collect_timer = 180  # 3 segundos

    def start_question(self):
        if not self.showing_question and not self.completed:
            self.question_screen = QuestionScreen(PREGUNTAS_APUS[self.scene_number])
            self.showing_question = True

    def handle_event(self, event, player):
        if self.showing_question and self.question_screen:
            self.question_screen.handle_input(event)
            
            if self.question_screen.is_finished():
                if self.question_screen.correct:
                    self.completed = True
                    self.door.open_door()
                    self.player_can_advance = True
                    
                    # El Apu entrega las illas robadas
                    illas_received = self.apu.give_illas_to_player(player, self.scene_number)
                    self.illas_message = f"¡Recibiste: {', '.join(illas_received)}!"
                    self.illas_message_timer = 300
                    
                    # Mostrar artículos visuales flotando
                    self.show_artikulos()
                    
                else:
                    if player.lose_life():
                        self.question_screen = QuestionScreen(PREGUNTAS_APUS[self.scene_number])
                    else:
                        return "GAME_OVER"
                
                self.showing_question = False
        
        return "CONTINUE"

    def update(self, player):
        self.apu.update()
        self.door.update()
        
        if self.question_screen:
            self.question_screen.update()
        
        # Actualizar artículos visuales
        for articulo in self.artikulos_visuales:
            articulo.update()
        
        # Auto-recolectar artículos después de un tiempo
        if hasattr(self, 'auto_collect_timer') and self.auto_collect_timer > 0:
            self.auto_collect_timer -= 1
            if self.auto_collect_timer <= 0:
                for articulo in self.artikulos_visuales:
                    articulo.collected = True
        
        if self.illas_message_timer > 0:
            self.illas_message_timer -= 1
        
        if not self.showing_question and not self.completed:
            if self.apu.rect.colliderect(player.rect):
                self.start_question()

    def draw(self, screen, player):
        font = pygame.font.SysFont("Arial", 20, bold=True)
        scene_text = font.render(f"Escena {self.scene_number + 1}/12 - {APUS_DATA[self.apu_name]['bioma']}", True, WHITE)
        screen.blit(scene_text, (10, 10))
        
        draw_pixelated_hearts(screen, player.lives, player.max_lives, 10, 40)
        
        illas_text = font.render(f"Illas Recuperadas: {len(player.articulos_collected)}/19", True, WHITE)
        screen.blit(illas_text, (10, 80))
        
        if self.illas_message_timer > 0:
            message_font = pygame.font.SysFont("Arial", 18, bold=True)
            message_surface = message_font.render(self.illas_message, True, GREEN)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
            
            padding = 10
            bg_rect = pygame.Rect(message_rect.x - padding, message_rect.y - padding,
                                message_rect.width + 2*padding, message_rect.height + 2*padding)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(180)
            bg_surface.fill(BLACK)
            screen.blit(bg_surface, bg_rect)
            
            screen.blit(message_surface, message_rect)
        
        # Dibujar artículos visuales flotantes
        for articulo in self.artikulos_visuales:
            articulo.draw(screen)
        
        if not self.completed:
            self.apu.draw(screen)
        self.door.draw(screen)
        
        if self.showing_question and self.question_screen:
            self.question_screen.draw(screen)

    def can_advance(self, player):
        return self.player_can_advance and self.door.rect.colliderect(player.rect)


class AnimatedBackground:
    def __init__(self, scene_number=0):
        self.scene_number = scene_number
        
        bioma_gif_path = BIOMA_GIFS[scene_number] if scene_number < len(BIOMA_GIFS) else None
        
        if bioma_gif_path and os.path.exists(bioma_gif_path):
            self.frames = load_gif_frames(bioma_gif_path)
            if self.frames:
                self.frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in self.frames]
                self.current_frame = 0
                self.animation_speed = 0.1
                self.animation_timer = 0
                self.use_gif = True
                print(f"🏔️ Cargado fondo animado: {bioma_gif_path}")
            else:
                print(f"❌ Error cargando GIF: {bioma_gif_path}")
                self.create_biome_background()
        else:
            print(f"📁 GIF no encontrado: {bioma_gif_path if bioma_gif_path else 'N/A'}, usando fondo estático")
            self.create_biome_background()

    def create_biome_background(self):
        self.use_gif = False
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        biome_colors = [
            (135, 206, 250, 100, 149, 237),  # Azul montaña
            (255, 140, 0, 255, 69, 0),       # Naranja volcán
            (176, 224, 230, 255, 255, 255),  # Blanco glaciar
            (154, 205, 50, 34, 139, 34),     # Verde altiplano
            (238, 203, 173, 205, 133, 63),   # Beige desierto
            (220, 20, 60, 139, 0, 0),        # Rojo volcán activo
            (240, 248, 255, 70, 130, 180),   # Azul claro nevado
            (112, 128, 144, 47, 79, 79),     # Gris cordillera
            (147, 112, 219, 75, 0, 130),     # Púrpura laguna
            (34, 139, 34, 0, 100, 0),        # Verde selva
            (255, 250, 205, 255, 215, 0),    # Amarillo valle
            (138, 43, 226, 75, 0, 130)       # Púrpura cima suprema
        ]
        
        if self.scene_number < len(biome_colors):
            sky_color = biome_colors[self.scene_number][:3]
            ground_color = biome_colors[self.scene_number][3:6]
        else:
            sky_color = (30, 30, 100)
            ground_color = (20, 80, 20)
        
        self.background.fill(sky_color)
        pygame.draw.rect(self.background, ground_color, (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150))

    def update(self):
        if self.use_gif:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        if self.use_gif:
            screen.blit(self.frames[self.current_frame], (0, 0))
        else:
            screen.blit(self.background, (0, 0))


# ================== GAME MANAGER ==================
class GameManager:
    def __init__(self):
        self.current_scene = 0
        self.total_scenes = 12
        self.scenes = []
        self.player = Player(100, SCREEN_HEIGHT - 250, gif_path="gif.gif", scale_factor=0.1)
        self.background = AnimatedBackground(scene_number=0)
        self.game_state = "MENU"  # 👉 empieza en menú
        self.font_big = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)

        # ✅ Menú principal
        self.main_menu = MainMenu()

        # ✅ Escenas
        for i in range(self.total_scenes):
            self.scenes.append(GameScene(i))

        # ✅ Música
        self.current_music = None
        self.load_menu_music()  # 🎵 suena música del menú apenas inicia



    # 🔽 LO NUEVO QUE DEBES AGREGAR AQUÍ
    def load_menu_music(self):
        menu_music_path = "inicio.mp3"  # 🎵 pon aquí tu archivo del menú
        if os.path.exists(menu_music_path) and menu_music_path != self.current_music:
         stop_music()
         play_music(menu_music_path)
         self.current_music = menu_music_path
         print("🎵 Música del MENÚ principal cargada")


    def load_biome_music(self, scene_number):
     if scene_number < len(BIOMA_MUSIC):
        music_path = BIOMA_MUSIC[scene_number]
        if os.path.exists(music_path) and music_path != self.current_music:
            stop_music()
            play_music(music_path)
            self.current_music = music_path
            print(f"🎵 Música del bioma {scene_number+1}: {music_path}")

    def handle_event(self, event):
        if self.game_state == "MENU":
            menu_result = self.main_menu.handle_input(event)
            if menu_result == "JUGAR":
                stop_music()
                self.game_state = "PLAYING"
                self.load_biome_music(0)
            elif menu_result == "INSTRUCCIONES":
                self.game_state = "INSTRUCTIONS"
            elif menu_result == "SALIR":
                return "QUIT"
                
        elif self.game_state == "INSTRUCTIONS":
            instr_result = self.instructions_screen.handle_input(event)
            if instr_result == "BACK":
                self.game_state = "MENU"
                
        elif self.game_state == "PLAYING":
            result = self.scenes[self.current_scene].handle_event(event, self.player)
            if result == "GAME_OVER":
                self.game_state = "GAME_OVER"
                stop_music()
                
        elif self.game_state in ["GAME_OVER", "VICTORY"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart_game()
                elif event.key == pygame.K_m:
                    stop_music()
                    self.game_state = "MENU"
                    if hasattr(self, 'main_menu') and hasattr(self.main_menu, 'menu_music_path'):
                        if os.path.exists(self.main_menu.menu_music_path):
                            play_music(self.main_menu.menu_music_path)
        
        return "CONTINUE"

    def update(self):
        if self.game_state == "MENU":
            self.main_menu.update()
        elif self.game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            self.player.update()
            
            self.scenes[self.current_scene].update(self.player)
            
            if self.scenes[self.current_scene].can_advance(self.player):
                self.advance_to_next_scene()
            
            self.background.update()

    def advance_to_next_scene(self):
     if self.current_scene < self.total_scenes - 1:
        self.current_scene += 1
        self.player.rect.x = 100
        self.player.rect.y = SCREEN_HEIGHT - 250
        self.background = AnimatedBackground(scene_number=self.current_scene)

        self.load_biome_music(self.current_scene)  # 🎵 cambia música
     else:
        self.game_state = "VICTORY"
        stop_music()



    def restart_game(self):
        self.current_scene = 0
        self.player = Player(100, SCREEN_HEIGHT - 250, gif_path="gif.gif", scale_factor=0.1)
        self.background = AnimatedBackground(scene_number=0)
        self.game_state = "PLAYING"
        
        self.scenes = []
        for i in range(self.total_scenes):
            self.scenes.append(GameScene(i))
        
        self.load_biome_music(0)

    def draw(self, screen):
        if self.game_state == "MENU":
            self.main_menu.draw(screen)
            
        elif self.game_state == "INSTRUCTIONS":
            self.main_menu.draw(screen)  # Fondo del menú
            self.instructions_screen.draw(screen)
            
        elif self.game_state == "PLAYING":
            self.background.draw(screen)
            self.player.draw(screen)
            self.scenes[self.current_scene].draw(screen, self.player)
            
            progress_text = self.font_medium.render(f"Progreso: {self.current_scene + 1}/{self.total_scenes}", True, WHITE)
            screen.blit(progress_text, (SCREEN_WIDTH - 200, 10))
            
        elif self.game_state == "GAME_OVER":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_text = self.font_big.render("¡GAME OVER!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))
            screen.blit(game_over_text, game_over_rect)
            
            score_text = self.font_medium.render(f"Llegaste hasta la escena {self.current_scene + 1}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(score_text, score_rect)
            
            articles_text = self.font_medium.render(f"Illas recuperadas: {len(self.player.articulos_collected)}/19", True, WHITE)
            articles_rect = articles_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(articles_text, articles_rect)
            
            restart_text = self.font_medium.render("Presiona 'R' para reiniciar | 'M' para menú", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_rect)
            
        elif self.game_state == "VICTORY":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            victory_text = self.font_big.render("¡VICTORIA TOTAL!", True, GREEN)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90))
            screen.blit(victory_text, victory_rect)
            
            completion_text = self.font_medium.render("¡Ekeko completó su aventura por los 12 Apus!", True, WHITE)
            completion_rect = completion_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(completion_text, completion_rect)
            
            articles_text = self.font_medium.render(
                f"Illas sagradas recuperadas: {len(self.player.articulos_collected)}/19", 
                True, YELLOW
            )
            articles_rect = articles_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 0))
            screen.blit(articles_text, articles_rect)
            
            restart_text = self.font_medium.render("Presiona 'R' para reiniciar | 'M' para menú", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_rect)
    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()
def main():
    game = GameManager()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()






                        