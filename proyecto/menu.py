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
    """
    Carga todos los frames de un archivo GIF como superficies de pygame.

    Args:
        gif_path (str): Ruta del archivo GIF a cargar.

    Returns:
        list[pygame.Surface] | None: Lista de frames convertidos a superficies de pygame,
        o None si ocurre un error o el archivo no existe.
    """
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
    """
    Reproduce una pista de música de fondo utilizando pygame.mixer.

    Args:
        music_path (str): Ruta del archivo de música (MP3 o WAV).
        loop (int, opcional): Cantidad de veces que se repite. Por defecto, -1 (infinito).

    Returns:
        bool: True si la música se reproduce correctamente, False si hay error.
    """
    try:
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loop)
            return True
        return False
    except Exception as e:
        print(f"Error reproduciendo música: {e}")
        return False


def stop_music():
    """
    Detiene cualquier música actualmente en reproducción.
    """
    pygame.mixer.music.stop()


class MainMenu:
    """
    Clase que representa el menú principal del juego.

    Permite mostrar el fondo animado, las opciones de menú y detectar
    la navegación del usuario mediante las teclas ↑, ↓ y ENTER.
    """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """
        Inicializa el menú principal, cargando fondos, texto y música.

        Args:
            SCREEN_WIDTH (int): Ancho de la pantalla.
            SCREEN_HEIGHT (int): Alto de la pantalla.
        """
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.selected_option = 0
        self.options = ["JUGAR", "INSTRUCCIONES", "SALIR"]
        self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_options = pygame.font.SysFont("Arial", 32, bold=True)
        
        # Carga de fondos animados (GIF)
        self.background_frames = None
        self.background_gif_paths = [
            "menu/menu_background.gif",
            "biomas/primerBio.gif",
            "biomas/segundoBio.gif",
            "illas/mochila.gif"
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
        
        # Si no hay fondo animado, crear fondo estático
        if not self.background_frames:
            self.create_enhanced_static_background()
        
        # Cargar GIF de Ekeko para animación del menú
        self.ekeko_frames = None
        ekeko_paths = ["gif.gif", "illas/mochila.gif"]
        for ekeko_path in ekeko_paths:
            if os.path.exists(ekeko_path):
                self.ekeko_frames = load_gif_frames(ekeko_path)
                if self.ekeko_frames:
                    ekeko_size = 120
                    self.ekeko_frames = [pygame.transform.scale(f, (ekeko_size, ekeko_size)) for f in self.ekeko_frames]
                    self.ekeko_current_frame = 0
                    self.ekeko_animation_timer = 0
                    self.ekeko_animation_speed = 0.15
                    print(f"🎮 GIF de Ekeko cargado para menú: {ekeko_path}")
                    break
        
        # Reproducir música de fondo del menú
        self.menu_music_path = "menu/inicio.mp3"
        if os.path.exists(self.menu_music_path):
            play_music(self.menu_music_path)
            print(f"🎵 Reproduciendo música del menú: {self.menu_music_path}")
        else:
            print("🎵 Archivo de música del menú no encontrado")

    def create_enhanced_static_background(self):
        """
        Crea un fondo estático colorido con montañas y cielo degradado
        para usar en caso de que no se cargue un GIF animado.
        """
        self.static_background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Cielo con degradado
        for y in range(self.SCREEN_HEIGHT):
            color_ratio = y / self.SCREEN_HEIGHT
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (255 - 206) * color_ratio)
            b = int(250 + (255 - 250) * color_ratio)
            pygame.draw.line(self.static_background, (r, g, b), (0, y), (self.SCREEN_WIDTH, y))
        
        # Montañas
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
        """
        Maneja la navegación del usuario dentro del menú principal.

        Args:
            event (pygame.event.Event): Evento detectado (tecla presionada).

        Returns:
            str | None: Nombre de la opción seleccionada ("JUGAR", "INSTRUCCIONES" o "SALIR"),
            o None si no se selecciona ninguna.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

    def update(self):
        """
        Actualiza los cuadros de animación del fondo y del Ekeko.
        """
        if self.background_frames:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.background_frames)
        
        if self.ekeko_frames:
            self.ekeko_animation_timer += self.ekeko_animation_speed
            if self.ekeko_animation_timer >= 1:
                self.ekeko_animation_timer = 0
                self.ekeko_current_frame = (self.ekeko_current_frame + 1) % len(self.ekeko_frames)

    def draw(self, screen):
        """
        Dibuja todos los elementos del menú en pantalla: fondo, texto y opciones.

        Args:
            screen (pygame.Surface): Superficie donde se renderiza el menú.
        """
        # Fondo animado o estático
        if self.background_frames:
            screen.blit(self.background_frames[self.current_frame], (0, 0))
        else:
            screen.blit(self.static_background, (0, 0))
        
        # Ekeko animado
        if self.ekeko_frames:
            ekeko_x = 50
            ekeko_y = self.SCREEN_HEIGHT - 200
            screen.blit(self.ekeko_frames[self.ekeko_current_frame], (ekeko_x, ekeko_y))
            ekeko_text = pygame.font.SysFont("Arial", 16, bold=True).render("Ekeko", True, WHITE)
            ekeko_text_rect = ekeko_text.get_rect(center=(ekeko_x + 60, ekeko_y + 130))
            screen.blit(ekeko_text, ekeko_text_rect)
        
        # Título principal
        title_text = self.font_title.render("LA TRAVESÍA DE EKEKO", True, WHITE)
        title_shadow = self.font_title.render("LA TRAVESÍA DE EKEKO", True, BLACK)
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, 120))
        shadow_rect = title_shadow.get_rect(center=(self.SCREEN_WIDTH // 2 + 4, 124))
        screen.blit(title_shadow, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.font_subtitle.render("Rescata las 19 Illas Sagradas de los 14 Apus", True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(self.SCREEN_WIDTH // 2, 170))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Opciones del menú
        start_y = 250
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = YELLOW
                pygame.draw.rect(screen, YELLOW, (self.SCREEN_WIDTH // 2 - 150, start_y + i * 60 - 10, 300, 50), 3)
            else:
                color = WHITE
            
            text_surface = self.font_options.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 60))
            screen.blit(text_surface, text_rect)
        
        # Texto de ayuda
        nav_text = pygame.font.SysFont("Arial", 18).render("Usa ↑↓ para navegar, ENTER para seleccionar", True, WHITE)
        nav_rect = nav_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 80))
        screen.blit(nav_text, nav_rect)


class InstructionsScreen:
    """
    Clase que representa la pantalla de instrucciones del juego.
    """

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """
        Inicializa la pantalla de instrucciones.

        Args:
            SCREEN_WIDTH (int): Ancho de la pantalla.
            SCREEN_HEIGHT (int): Alto de la pantalla.
        """
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.font_title = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 18)
        
    def handle_input(self, event):
        """
        Detecta las teclas de salida (ESC o ENTER) para volver al menú principal.

        Args:
            event (pygame.event.Event): Evento del teclado.

        Returns:
            str | None: "BACK" si se presiona ESC o ENTER, None en caso contrario.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "BACK"
        return None
    
    def draw(self, screen):
        """
        Llama a la función encargada de dibujar las instrucciones.

        Args:
            screen (pygame.Surface): Superficie de pygame donde se dibujan las instrucciones.
        """
        from instrucciones import dibujar_instrucciones
        dibujar_instrucciones(screen, self.font_title, self.font_text, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
