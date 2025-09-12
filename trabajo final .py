import pygame
import sys
import os
import random
import math  # 👈 Para coseno y demás
from PIL import Image

# ================== PYGAME INICIO ==================
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aventura de Ekeko - Pygame con Árbol Binario")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# ================== DATOS ==================
APUS_DATA = {
    "Huascarán": {"color": (255, 255, 255), "health": 100, "speed": 2, "size": 80},
    "Misti": {"color": (255, 150, 150), "health": 85, "speed": 3, "size": 70},
    "Coropuna": {"color": (200, 200, 255), "health": 90, "speed": 2.5, "size": 75},
}

ARTICULOS_DATA = [
    "Tumi", "Chacana", "Illa", "Torito", "Papa", "Maíz", "Inti", "Killa", "Chaska"
]

# ================== ÁRBOL BINARIO ==================
class NodoArbol:
    def __init__(self, valor, tipo="articulo"):
        self.valor = valor
        self.tipo = tipo  # "apu" o "articulo"
        self.izquierda = None
        self.derecha = None

class ArbolJerarquico:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor, tipo="articulo"):
        nuevo = NodoArbol(valor, tipo)
        if not self.raiz:
            self.raiz = nuevo
        else:
            self._insertar(self.raiz, nuevo)

    def _insertar(self, nodo, nuevo):
        if nuevo.valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = nuevo
            else:
                self._insertar(nodo.izquierda, nuevo)
        else:
            if nodo.derecha is None:
                nodo.derecha = nuevo
            else:
                self._insertar(nodo.derecha, nuevo)

    def mostrar_inorden(self, nodo=None):
        if nodo is None:
            nodo = self.raiz
            if nodo is None:
                return
        if nodo.izquierda:
            self.mostrar_inorden(nodo.izquierda)
        print(f"{nodo.tipo.upper()} → {nodo.valor}")
        if nodo.derecha:
            self.mostrar_inorden(nodo.derecha)

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

# ================== CLASES ==================
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
        self.health = 100
        self.max_health = 100
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

    def collect_articulo(self, articulo_name):
        if articulo_name not in self.articulos_collected:
            self.articulos_collected.append(articulo_name)
            print(f"🎒 Ekeko recolectó: {articulo_name}")
            return True
        return False

    def draw(self, screen):
        # Dibuja al jugador
        screen.blit(self.image, self.rect)
        # Barra de vida
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 15, 60, 8))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 15,
                                         int((self.health / self.max_health) * 60), 8))
        # Nombre
        text_surface = self.font.render("Ekeko", True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(text_surface, text_rect)


class Apu:
    def __init__(self, name, x, y, gif_path=None):
        self.name = name
        self.data = APUS_DATA[name]
        self.size = self.data["size"]
        self.health = self.data["health"]
        self.max_health = self.data["health"]
        self.speed = self.data["speed"]

        self.frames = None
        if gif_path and os.path.exists(gif_path):
            self.frames = load_gif_frames(gif_path)
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
        self.vel_x = random.choice([-1, 1]) * self.speed
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.8
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.active = True
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

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
        if abs(self.rect.centerx - player.rect.centerx) < 200:
            if self.rect.centerx < player.rect.centerx:
                self.vel_x = abs(self.vel_x)
            else:
                self.vel_x = -abs(self.vel_x)
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.original_frames)
            self.image = self.original_frames[self.frame_index]
        if self.rect.colliderect(player.rect):
            player.health -= 1

    def draw(self, screen):
        if not self.active:
            return
        # Sprite
        screen.blit(self.image, self.rect)
        # Barra de vida
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, 80, 10))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 20,
                                         int((self.health / self.max_health) * 80), 10))
        # Nombre
        text_surface = self.font.render(self.name, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(text_surface, text_rect)


class Articulo:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
        self.color = (255, 255, 0)
        self.float_timer = 0
        self.base_y = y
        self.font = pygame.font.SysFont("Arial", 14, bold=True)

    def update(self):
        if not self.collected:
            self.float_timer += 0.1
            self.rect.y = self.base_y + int(5 * math.cos(self.float_timer))

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, self.color, self.rect.center, 10)
            pygame.draw.circle(screen, WHITE, self.rect.center, 10, 2)
            # Nombre debajo
            text_surface = self.font.render(self.name, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))
            screen.blit(text_surface, text_rect)


# ================== GAME STATE ==================
class GameState:
    def __init__(self):
        self.articulos = []
        self.apus = []
        self.arbol = ArbolJerarquico()
        self.spawn_articulos()
        self.spawn_apus()
        self.crear_jerarquia()

    def spawn_articulos(self):
        for articulo_name in ARTICULOS_DATA:
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = SCREEN_HEIGHT - 200
            self.articulos.append(Articulo(articulo_name, x, y))

    def spawn_apus(self):
     for i, apu_name in enumerate(APUS_DATA.keys()):
        if apu_name == "Coropuna":
            apu = Apu(apu_name, 100 + i * 150, SCREEN_HEIGHT - 230, gif_path="-1--unscreen.gif")
        elif apu_name == "Huascarán":
            apu = Apu(apu_name, 100 + i * 150, SCREEN_HEIGHT - 230, gif_path="-1--unscreen.gif")
        else:
            apu = Apu(apu_name, 100 + i * 150, SCREEN_HEIGHT - 230, gif_path="-1--unscreen.gif")
        self.apus.append(apu)


    def crear_jerarquia(self):
        for apu in self.apus:
            self.arbol.insertar(apu.name, tipo="apu")
        for articulo in self.articulos:
            self.arbol.insertar(articulo.name, tipo="articulo")

        print("📌 Jerarquía del Árbol (Inorden):")
        self.arbol.mostrar_inorden()

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

# ================== FONDO ==================
class AnimatedBackground:
    def __init__(self, gif_path=None):
        if gif_path and os.path.exists(gif_path):
            self.frames = load_gif_frames(gif_path)
            if self.frames:
                self.frames = [pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in self.frames]
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

# ================== MAIN ==================
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

