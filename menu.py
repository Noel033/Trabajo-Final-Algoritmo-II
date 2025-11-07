# ================== SISTEMA DE MENÚ ==================
# Archivo separado con todas las clases y funciones del menú
# Para mantener el código principal más limpio y organizado

import pygame
import os

# Colores del menú
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 100, 0)
GRAY = (128, 128, 128)

def load_gif_frames(gif_path):
    """Carga todos los frames de un GIF como superficies pygame"""
    try:
        from PIL import Image
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

def play_music(music_path, loop=-1):
    """Reproduce música de fondo"""
    try:
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loop)  # -1 = loop infinito
            return True
        return False
    except Exception as e:
        print(f"Error reproduciendo música: {e}")
        return False

def stop_music():
    """Detiene la música de fondo"""
    pygame.mixer.music.stop()

class MainMenu:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.selected_option = 0
        self.options = ["JUGAR", "INSTRUCCIONES", "SALIR"]
        self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_options = pygame.font.SysFont("Arial", 32, bold=True)
        
        # 🎨 MEJORADO: Cargar fondo del menú con múltiples opciones
        self.background_frames = None
        self.background_gif_paths = [
            "menu/menu_background.gif",
            "biomas/Adobe Express - Video_de_Lluvia_de_Hamburguesas.gif",  # Fallback 1
            "biomas/segundoBio.gif", # Fallback 2
            "illas/mochila.gif"     # Fallback 3
        ]
        
        for bg_path in self.background_gif_paths:
            if os.path.exists(bg_path):
                self.background_frames = load_gif_frames(bg_path)
                if self.background_frames:
                    self.background_frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in self.background_frames]
                    self.current_frame = 0
                    self.animation_timer = 0
                    self.animation_speed = 0.1
                    print(f"🎨 Fondo del menú cargado: {bg_path}")
                    break
        
        # Si no hay GIF, crear fondo estático mejorado
        if not self.background_frames:
            self.create_enhanced_static_background()
        
        # 🎮 MEJORADO: Cargar GIF de Ekeko para el menú
        self.ekeko_frames = None
        ekeko_paths = ["ekeko.gif", "mochila.gif"]
        for ekeko_path in ekeko_paths:
            if os.path.exists(ekeko_path):
                self.ekeko_frames = load_gif_frames(ekeko_path)
                if self.ekeko_frames:
                    # Redimensionar Ekeko para el menú
                    ekeko_size = 120
                    self.ekeko_frames = [pygame.transform.scale(f, (ekeko_size, ekeko_size)) for f in self.ekeko_frames]
                    self.ekeko_current_frame = 0
                    self.ekeko_animation_timer = 0
                    self.ekeko_animation_speed = 0.15
                    print(f"🎮 GIF de Ekeko cargado para menú: {ekeko_path}")
                    break
        
        # Cargar y reproducir música del menú
        self.menu_music_path = "music/Determination.mp3"  # Ruta actualizada
        # Intentar varias opciones de música
        music_options = [
            "music/Determination.mp3",
            "music/It's Showtime!.mp3",
            "music/Nevado1.mp3",
            "music/Musica3.mp3"
        ]
        for music_path in music_options:
            if os.path.exists(music_path):
                self.menu_music_path = music_path
                break
        
        if os.path.exists(self.menu_music_path):
            play_music(self.menu_music_path)
            print(f"🎵 Reproduciendo música del menú: {self.menu_music_path}")
        else:
            print("🎵 Archivo de música del menú no encontrado")

    def create_enhanced_static_background(self):
        """Crear fondo estático mejorado con montañas"""
        self.static_background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Degradado de cielo andino
        for y in range(self.SCREEN_HEIGHT):
            color_ratio = y / self.SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(250 + (255 - 250) * color_ratio)
            pygame.draw.line(self.static_background, (r, g, b), (0, y), (self.SCREEN_WIDTH, y))
        
        # Montañas de fondo
        mountain_points = [
            (0, self.SCREEN_HEIGHT - 200),
            (200, self.SCREEN_HEIGHT - 300),
            (400, self.SCREEN_HEIGHT - 250),
            (600, self.SCREEN_HEIGHT - 350),
            (800, self.SCREEN_HEIGHT - 200),
            (800, self.SCREEN_HEIGHT),
            (0, self.SCREEN_HEIGHT)
        ]
        pygame.draw.polygon(self.static_background, (100, 100, 100), mountain_points)
        
        # Suelo verde
        pygame.draw.rect(self.static_background, (34, 139, 34), (0, self.SCREEN_HEIGHT - 150, self.SCREEN_WIDTH, 150))

    def handle_input(self, event):
        """🎮 BOTONES PARA NAVEGAR EN EL MENÚ:
        - ↑↓: Navegar entre opciones del menú
        - ENTER: Seleccionar opción
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:  # 🎮 BOTÓN ARRIBA
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:  # 🎮 BOTÓN ABAJO
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:  # 🎮 BOTÓN SELECCIONAR
                return self.options[self.selected_option]
        return None

    def update(self):
        # Actualizar animación del fondo
        if self.background_frames:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.background_frames)
        
        # Actualizar animación de Ekeko
        if self.ekeko_frames:
            self.ekeko_animation_timer += self.ekeko_animation_speed
            if self.ekeko_animation_timer >= 1:
                self.ekeko_animation_timer = 0
                self.ekeko_current_frame = (self.ekeko_current_frame + 1) % len(self.ekeko_frames)

    def draw(self, screen):
        # Dibujar fondo
        if self.background_frames:
            screen.blit(self.background_frames[self.current_frame], (0, 0))
        else:
            screen.blit(self.static_background, (0, 0))
        
        # Dibujar GIF de Ekeko animado en la esquina
        if self.ekeko_frames:
            ekeko_x = 50
            ekeko_y = self.SCREEN_HEIGHT - 200
            screen.blit(self.ekeko_frames[self.ekeko_current_frame], (ekeko_x, ekeko_y))
            
            # Texto "Ekeko" debajo del GIF
            ekeko_text = pygame.font.SysFont("Arial", 16, bold=True).render("Ekeko", True, WHITE)
            ekeko_text_rect = ekeko_text.get_rect(center=(ekeko_x + 60, ekeko_y + 130))
            screen.blit(ekeko_text, ekeko_text_rect)
        
        # Título principal con efecto de sombra mejorado
        title_text = self.font_title.render("LA TRAVESÍA DE EKEKO", True, WHITE)
        title_shadow = self.font_title.render("LA TRAVESÍA DE EKEKO", True, BLACK)
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, 120))
        shadow_rect = title_shadow.get_rect(center=(self.SCREEN_WIDTH // 2 + 4, 120 + 4))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Subtítulo mejorado
        subtitle_text = self.font_subtitle.render("Rescata las 19 Illas Sagradas de los 14 Apus", True, YELLOW)
        subtitle_shadow = self.font_subtitle.render("Rescata las 19 Illas Sagradas de los 14 Apus", True, BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(self.SCREEN_WIDTH // 2, 170))
        subtitle_shadow_rect = subtitle_shadow.get_rect(center=(self.SCREEN_WIDTH // 2 + 2, 170 + 2))
        screen.blit(subtitle_shadow, subtitle_shadow_rect)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú con diseño mejorado
        start_y = 250
        for i, option in enumerate(self.options):
            # Colores dinámicos según selección
            if i == self.selected_option:
                color = YELLOW
                shadow_color = BLACK
                # Efecto de resaltado
                highlight_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 150, start_y + i * 60 - 10, 300, 50)
                pygame.draw.rect(screen, (255, 255, 0, 50), highlight_rect)
                pygame.draw.rect(screen, YELLOW, highlight_rect, 3)
            else:
                color = WHITE
                shadow_color = BLACK
            
            text_surface = self.font_options.render(option, True, color)
            shadow_surface = self.font_options.render(option, True, shadow_color)
            
            text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 60))
            shadow_rect = shadow_surface.get_rect(center=(self.SCREEN_WIDTH // 2 + 3, start_y + i * 60 + 3))
            
            screen.blit(shadow_surface, shadow_rect)
            screen.blit(text_surface, text_rect)
        
        # Instrucciones de navegación mejoradas
        nav_text = pygame.font.SysFont("Arial", 18).render("Usa ↑↓ para navegar, ENTER para seleccionar", True, WHITE)
        nav_shadow = pygame.font.SysFont("Arial", 18).render("Usa ↑↓ para navegar, ENTER para seleccionar", True, BLACK)
        nav_rect = nav_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 80))
        nav_shadow_rect = nav_shadow.get_rect(center=(self.SCREEN_WIDTH // 2 + 1, self.SCREEN_HEIGHT - 79))
        screen.blit(nav_shadow, nav_shadow_rect)
        screen.blit(nav_text, nav_rect)
        
        # Información adicional
        info_text = pygame.font.SysFont("Arial", 14).render("Presiona ESC para salir del juego", True, GRAY)
        info_rect = info_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 40))
        screen.blit(info_text, info_rect)

class InstructionsScreen:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 18)
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "BACK"
        return None
    
    def draw(self, screen):
        # Importar función de instrucciones
        from instrucciones import dibujar_instrucciones
        dibujar_instrucciones(screen, self.font_title, self.font_text, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
