import pygame
import sys
import os
import random
import math  # 👈 IMPORTAR math para cos, sin, etc.
from PIL import Image

# Inicializar Pygame
pygame.init()

# Configuraciones de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aventura de Ekeko - Pygame")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Configuraciones del juego
FPS = 60
clock = pygame.time.Clock()

# 🏔️ DATOS DE LOS APUS (Jefes)
APUS_DATA = {
    "Huascarán": {"color": (255, 255, 255), "health": 100, "speed": 2, "size": 80},
    "Coropuna": {"color": (200, 200, 255), "health": 90, "speed": 2.5, "size": 75},
    "Misti": {"color": (255, 150, 150), "health": 85, "speed": 3, "size": 70},
    "Ampato": {"color": (150, 255, 150), "health": 95, "speed": 2.2, "size": 78},
    "Sara Sara": {"color": (255, 200, 100), "health": 80, "speed": 3.2, "size": 65},
    "Salkantay": {"color": (100, 200, 255), "health": 110, "speed": 1.8, "size": 85},
    "Chachani": {"color": (200, 100, 255), "health": 88, "speed": 2.8, "size": 72},
    "Ccarhuarazo": {"color": (255, 100, 200), "health": 92, "speed": 2.3, "size": 76},
    "Rasuwillka": {"color": (100, 255, 200), "health": 87, "speed": 2.9, "size": 68},
    "Hualca Hualca": {"color": (255, 255, 100), "health": 93, "speed": 2.4, "size": 74},
    "Huarancante": {"color": (200, 255, 200), "health": 89, "speed": 2.7, "size": 71},
    "Allincapac": {"color": (255, 200, 200), "health": 96, "speed": 2.1, "size": 79}
}

# 🎒 DATOS DE LOS ARTÍCULOS
ARTICULOS_DATA = [
    "Tumi", "Chacana", "Illa", "Torito", "Perro Viringo", "Cuy", "Qullqi", "Quispe",
    "Qori", "Chuño", "Papa", "Maíz", "Calluha", "Cungalpo", "Hizanche", "Huashacara",
    "Inti", "Killa", "Chaska"
]

def load_gif_frames(gif_path):
    """Carga todos los frames de un GIF y los convierte a superficies de Pygame"""
    try:
        gif = Image.open(gif_path)
        frames = []
        
        for frame_num in range(gif.n_frames):
            gif.seek(frame_num)
            frame = gif.copy()
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            frame_data = frame.tobytes()
            frame_surface = pygame.image.fromstring(frame_data, frame.size, 'RGBA')
            frames.append(frame_surface)
        
        return frames
    except Exception as e:
        print(f"Error cargando GIF {gif_path}: {e}")
        return None

class Player:
    def __init__(self, x, y, gif_path=None, scale_factor=1.0):
        self.scale_factor = scale_factor
        if gif_path and os.path.exists(gif_path):
            self.frames = load_gif_frames(gif_path)
            if self.frames:
                if scale_factor != 1.0:
                    scaled_frames = []
                    for frame in self.frames:
                        original_size = frame.get_size()
                        new_width = int(original_size[0] * scale_factor)
                        new_height = int(original_size[1] * scale_factor)
                        scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
                        scaled_frames.append(scaled_frame)
                    self.frames = scaled_frames
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
        
        self.health = 100
        self.max_health = 100
        self.articulos_collected = []
        
    def create_placeholder(self):
        self.frames = []
        width = int(40 * self.scale_factor)
        height = int(60 * self.scale_factor)
        colors = [(255, 100, 100), (100, 255, 100), (150, 100, 255), (255, 150, 100)]
        for i in range(4):
            frame = pygame.Surface((width, height), pygame.SRCALPHA)
            frame.fill(colors[i])
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
            if not self.facing_right:
                self.image = pygame.transform.flip(self.original_frames[0], True, False)
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
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def collect_articulo(self, articulo_name):
        if articulo_name not in self.articulos_collected:
            self.articulos_collected.append(articulo_name)
            print(f"🎒 Ekeko recolectó: {articulo_name}")
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        health_bar_width = 60
        health_bar_height = 8
        health_x = self.rect.x
        health_y = self.rect.y - 15
        pygame.draw.rect(screen, RED, (health_x, health_y, health_bar_width, health_bar_height))
        current_health_width = int((self.health / self.max_health) * health_bar_width)
        pygame.draw.rect(screen, GREEN, (health_x, health_y, current_health_width, health_bar_height))

class Apu:
    def __init__(self, name, x, y, gif_path=None):
        self.name = name
        self.data = APUS_DATA[name]
        if gif_path and os.path.exists(gif_path):
            self.frames = load_gif_frames(gif_path)
            if self.frames:
                size = self.data["size"]
                self.frames = [pygame.transform.scale(frame, (size, size)) for frame in self.frames]
                self.image = self.frames[0]
                self.original_frames = self.frames[:]
            else:
                self.create_placeholder()
        else:
            self.create_placeholder()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = self.data["health"]
        self.max_health = self.data["health"]
        self.speed = self.data["speed"]
        self.vel_x = random.choice([-1, 1]) * self.speed
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.8
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.active = True

    def create_placeholder(self):
        size = self.data["size"]
        color = self.data["color"]
        self.frames = []
        for i in range(3):
            frame = pygame.Surface((size, size), pygame.SRCALPHA)
            variation = 20 * i
            adjusted_color = tuple(min(255, max(0, c + variation)) for c in color)
            pygame.draw.circle(frame, adjusted_color, (size//2, size//2), size//2 - 5)
            eye_size = size // 10
            pygame.draw.circle(frame, BLACK, (size//3, size//3), eye_size)
            pygame.draw.circle(frame, BLACK, (2*size//3, size//3), eye_size)
            self.frames.append(frame)
        self.image = self.frames[0]
        self.original_frames = self.frames[:]

    def update(self, player):
        if not self.active:
            return
        if not self.on_ground:
            self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.vel_x *= -1
        ground_level = SCREEN_HEIGHT - 150
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        distance_to_player = abs(self.rect.centerx - player.rect.centerx)
        if distance_to_player < 200:
            if self.rect.centerx < player.rect.centerx:
                self.vel_x = abs(self.vel_x)
            else:
                self.vel_x = -abs(self.vel_x)
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.original_frames[self.frame_index]
        if self.rect.colliderect(player.rect):
            player.health -= 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False

    def draw(self, screen):
        if not self.active:
            return
        screen.blit(self.image, self.rect)
        health_bar_width = 80
        health_bar_height = 10
        health_x = self.rect.x
        health_y = self.rect.y - 20
        pygame.draw.rect(screen, RED, (health_x, health_y, health_bar_width, health_bar_height))
        current_health_width = int((self.health / self.max_health) * health_bar_width)
        pygame.draw.rect(screen, GREEN, (health_x, health_y, current_health_width, health_bar_height))
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.name, True, WHITE)
        screen.blit(name_text, (self.rect.x, self.rect.y - 35))

class Articulo:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
        color_map = {
            "Tumi": YELLOW, "Chacana": PURPLE, "Illa": BLUE, "Torito": RED,
            "Perro Viringo": (139, 69, 19), "Cuy": (160, 82, 45), "Qullqi": WHITE,
            "Quispe": (192, 192, 192), "Qori": YELLOW, "Chuño": (75, 0, 130),
            "Papa": (139, 69, 19), "Maíz": YELLOW, "Calluha": GREEN,
            "Cungalpo": (255, 140, 0), "Hizanche": (255, 20, 147),
            "Huashacara": (0, 255, 255), "Inti": (255, 215, 0),
            "Killa": (211, 211, 211), "Chaska": (255, 255, 255)
        }
        self.color = color_map.get(name, WHITE)
        self.float_timer = 0
        self.base_y = y

    def update(self):
        if not self.collected:
            self.float_timer += 0.1
            self.rect.y = self.base_y + int(5 * math.cos(self.float_timer))  # 👈 USAR math.cos

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, self.color, self.rect.center, 10)
            pygame.draw.circle(screen, WHITE, self.rect.center, 10, 2)
            font = pygame.font.Font(None, 16)
            text = font.render(self.name, True, WHITE)
            text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 15))
            screen.blit(text, text_rect)

class GameState:
    def __init__(self):
        self.articulos = []
        self.apus = []
        self.spawn_articulos()
        self.spawn_apu()

    def spawn_articulos(self):
        for i, articulo_name in enumerate(ARTICULOS_DATA):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = SCREEN_HEIGHT - 200 - random.randint(0, 100)
            self.articulos.append(Articulo(articulo_name, x, y))

    def spawn_apu(self):
            huascaran = Apu("Huascarán", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 230, gif_path="-1--unscreen.gif")
            self.apus.append(huascaran)


    def update(self, player):
        for articulo in self.articulos:
            articulo.update()
            if not articulo.collected and articulo.rect.colliderect(player.rect):
                articulo.collected = True
                player.collect_articulo(articulo.name)
        for apu in self.apus:
            apu.update(player)

    def draw(self, screen):
        for articulo in self.articulos:
            articulo.draw(screen)
        for apu in self.apus:
            apu.draw(screen)



class AnimatedBackground:
    def __init__(self, gif_path=None):
        if gif_path and os.path.exists(gif_path):
            self.frames = load_gif_frames(gif_path)
            if self.frames:
                self.frames = [pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT)) for frame in self.frames]
                self.current_frame = 0
                self.animation_speed = 0.1
                self.animation_timer = 0
                self.use_gif = True
            else:
                self.create_static_background()
        else:
            self.create_static_background()

    def create_static_background(self):
        self.use_gif = False
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((30, 30, 100))
        pygame.draw.rect(self.background, (20, 80, 20), (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 150))

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

# ------------------ MAIN LOOP ------------------
def main():
    # 🌄 Fondo animado (GIF del paisaje)
    background = AnimatedBackground(gif_path="1366_2000.gif")

    # 🎭 Ekeko (jugador) con su GIF y tamaño reducido al 50%
    # 👉 Cambia el número en scale_factor (ej: 0.5 = pequeño, 1.0 = normal, 1.5 = más grande)
    player = Player(100, SCREEN_HEIGHT - 250, gif_path="gif.gif", scale_factor=0.1)

    # 🏔️ Estado del juego (incluye Apus)
    game_state = GameState()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ⌨️ Controles
        keys = pygame.key.get_pressed()
        player.handle_input(keys)

        # 🔄 Actualizaciones
        player.update()
        game_state.update(player)
        background.update()

        # 🎨 Dibujos
        background.draw(screen)
        player.draw(screen)
        game_state.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()
