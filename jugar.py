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
pygame.display.set_caption("La Travesía de Ekeko - 14 Escenas")

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

# ================== ÁRBOL BINARIO PARA APUS ==================
class NodoApu:
    """Nodo del árbol binario que representa un Apu"""
    def __init__(self, nombre, datos):
        self.nombre = nombre
        self.datos = datos  # Contiene color, health, bioma, gif
        self.izquierda = None
        self.derecha = None

class ArbolApus:
    """Árbol binario para gestionar los 12 Apus del juego
    
    FUNCIONAMIENTO DEL ÁRBOL BINARIO:
    - Se ordena alfabéticamente por nombre del Apu
    - Al insertar: nombres menores van a la izquierda, mayores a la derecha
    - Al buscar: compara alfabéticamente y navega por el árbol
    - Al recorrer: visita izquierda → raíz → derecha (orden alfabético)
    - Al cambiar de nivel: se mueve automáticamente según la comparación alfabética
    """
    def __init__(self):
        self.raiz = None
        self.total_apus = 0
    
    def insertar(self, nombre, datos):
        """Inserta un nuevo Apu en el árbol binario ordenado alfabéticamente"""
        if self.raiz is None:
            self.raiz = NodoApu(nombre, datos)  # # INSERTAR APU: Raíz del árbol
            self.total_apus += 1
            print(f"🌳 Insertando {nombre} como RAÍZ del árbol")
        else:
            self._insertar_recursivo(self.raiz, nombre, datos)
    
    def _insertar_recursivo(self, nodo, nombre, datos):
        """Método recursivo para insertar un Apu - ORDENA ALFABÉTICAMENTE"""
        if nombre < nodo.nombre:
            if nodo.izquierda is None:
                nodo.izquierda = NodoApu(nombre, datos)  # # INSERTAR APU: Hijo izquierdo
                self.total_apus += 1
                print(f"🌳 Insertando {nombre} a la IZQUIERDA de {nodo.nombre}")
            else:
                self._insertar_recursivo(nodo.izquierda, nombre, datos)
        elif nombre > nodo.nombre:
            if nodo.derecha is None:
                nodo.derecha = NodoApu(nombre, datos)  # # INSERTAR APU: Hijo derecho
                self.total_apus += 1
                print(f"🌳 Insertando {nombre} a la DERECHA de {nodo.nombre}")
            else:
                self._insertar_recursivo(nodo.derecha, nombre, datos)
    
    def buscar(self, nombre):
        """Busca un Apu por su nombre en el árbol - NAVEGA POR NIVELES"""
        return self._buscar_recursivo(self.raiz, nombre)
    
    def _buscar_recursivo(self, nodo, nombre):
        """Método recursivo para buscar un Apu - RECORRE NIVELES DEL ÁRBOL"""
        if nodo is None:
            return None
        if nodo.nombre == nombre:
            return nodo
        elif nombre < nodo.nombre:
            return self._buscar_recursivo(nodo.izquierda, nombre)  # Baja al nivel izquierdo
        else:
            return self._buscar_recursivo(nodo.derecha, nombre)  # Baja al nivel derecho
    
    def recorrer_inorden(self):
        """Recorre el árbol en orden (izquierda, raíz, derecha) - ORDEN ALFABÉTICO"""
        apus_ordenados = []
        self._inorden_recursivo(self.raiz, apus_ordenados)
        return apus_ordenados
    
    def _inorden_recursivo(self, nodo, lista):
        """Recorrido inorden recursivo - VISITA TODOS LOS NIVELES"""
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierda, lista)  # Recorre subárbol izquierdo
            lista.append(nodo)  # Procesa nodo actual
            self._inorden_recursivo(nodo.derecha, lista)  # Recorre subárbol derecho
    
    def obtener_apu_por_indice(self, indice):
        """Obtiene un Apu por su índice en el recorrido inorden"""
        apus_ordenados = self.recorrer_inorden()
        if 0 <= indice < len(apus_ordenados):
            return apus_ordenados[indice]
        return None
    
    def obtener_datos_apu(self, nombre):
        """Obtiene los datos de un Apu por su nombre"""
        nodo = self.buscar(nombre)
        if nodo:
            return nodo.datos
        return None
    
    def mostrar_arbol(self):
        """Muestra la estructura del árbol (para debugging)"""
        print("=== ÁRBOL BINARIO DE APUS ===")
        self._mostrar_recursivo(self.raiz, 0)
        print(f"Total de Apus: {self.total_apus}")
    
    def _mostrar_recursivo(self, nodo, nivel):
        """Muestra recursivamente la estructura del árbol - MUESTRA NIVELES"""
        if nodo is not None:
            self._mostrar_recursivo(nodo.derecha, nivel + 1)
            print("  " * nivel + f"├─ {nodo.nombre} ({nodo.datos['bioma']})")
            self._mostrar_recursivo(nodo.izquierda, nivel + 1)

# ================== CLASES ESPECÍFICAS PARA CADA APU CON SU BIOMA ==================

class ApuBase:
    """Clase base para todos los Apus"""
    def __init__(self, nombre, color, health, bioma, gif):
        self.nombre = nombre
        self.color = color
        self.health = health
        self.bioma = bioma
        self.gif = gif
        self.illas_robadas = []
    
    def get_datos(self):
        """Retorna los datos del Apu en formato compatible con el árbol binario"""
        return {
            "color": self.color,
            "health": self.health,
            "bioma": self.bioma,
            "gif": self.gif
        }

class ApuHuascaran(ApuBase):
    """Apu Huascarán - Montaña Nevada"""
    def __init__(self):
        super().__init__(
            nombre="Huascarán",
            color=(255, 255, 255),
            health=100,
            bioma="Montaña Nevada",
            gif="Huascaran.gif"
        )
        self.illas_robadas = ["Tumi", "Chacana"]
        self.altura = 6768  # metros
        self.caracteristicas = ["Pico más alto del Perú", "Nevado permanente", "Parque Nacional"]

class ApuCoropuna(ApuBase):
    """Apu Coropuna - Glaciar"""
    def __init__(self):
        super().__init__(
            nombre="Coropuna",
            color=(200, 200, 255),
            health=90,
            bioma="Glaciar",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Perro Viringo", "Cuy"]
        self.altura = 6425  # metros
        self.caracteristicas = ["Volcán extinto", "Glaciar extenso", "Reserva natural"]

class ApuMisti(ApuBase):
    """Apu Misti - Volcán"""
    def __init__(self):
        super().__init__(
            nombre="Misti",
            color=(255, 150, 150),
            health=85,
            bioma="Volcán",
            gif="Misti.gif"
        )
        self.illas_robadas = ["Illa", "Torito"]
        self.altura = 5822  # metros
        self.caracteristicas = ["Volcán activo", "Cerca de Arequipa", "Forma cónica perfecta"]

class ApuAmpato(ApuBase):
    """Apu Ampato - Altiplano"""
    def __init__(self):
        super().__init__(
            nombre="Ampato",
            color=(150, 255, 150),
            health=95,
            bioma="Altiplano",
            gif="Ampato.gif"
        )
        self.illas_robadas = ["Qullqi", "Quispe"]
        self.altura = 6288  # metros
        self.caracteristicas = ["Volcán inactivo", "Zona de altiplano", "Clima frío"]

class ApuSaraSara(ApuBase):
    """Apu Sara Sara - Volcán Andino"""
    def __init__(self):
        super().__init__(
            nombre="Sara Sara",
            color=(255, 100, 100),
            health=88,
            bioma="Volcán Andino",
            gif="SaraSara.gif"
        )
        self.illas_robadas = ["Papa", "Maíz"]
        self.altura = 5505  # metros
        self.caracteristicas = ["Volcán andino", "Zona de Ayacucho", "Forma cónica"]

class ApuSalkantay(ApuBase):
    """Apu Salkantay - Selva Alta"""
    def __init__(self):
        super().__init__(
            nombre="Salkantay",
            color=(100, 255, 200),
            health=90,
            bioma="Selva Alta",
            gif="Salkantay.gif"
        )
        self.illas_robadas = ["Huashacara"]
        self.altura = 6271  # metros
        self.caracteristicas = ["Transición a selva", "Biodiversidad única", "Camino a Machu Picchu"]

class ApuChachani(ApuBase):
    """Apu Chachani - Desierto Alto"""
    def __init__(self):
        super().__init__(
            nombre="Chachani",
            color=(255, 200, 100),
            health=80,
            bioma="Desierto Alto",
            gif="Chachani.gif"
        )
        self.illas_robadas = ["Qori", "Chuño"]
        self.altura = 6057  # metros
        self.caracteristicas = ["Volcán extinto", "Desierto de altura", "Arena volcánica"]

class ApuCcarhuarazo(ApuBase):
    """Apu Ccarhuarazo - Cordillera Central"""
    def __init__(self):
        super().__init__(
            nombre="Ccarhuarazo",
            color=(180, 180, 255),
            health=92,
            bioma="Cordillera Central",
            gif="Ccarhuarazo.gif"
        )
        self.illas_robadas = ["Cungalpo"]
        self.altura = 5120  # metros
        self.caracteristicas = ["Cordillera central", "Zona de Huancavelica", "Nevado"]

class ApuRasuwillka(ApuBase):
    """Apu Rasuwillka - Montaña Sagrada"""
    def __init__(self):
        super().__init__(
            nombre="Rasuwillka",
            color=(255, 180, 255),
            health=95,
            bioma="Montaña Sagrada",
            gif="Rasuwillka.gif"
        )
        self.illas_robadas = ["Hizanche"]
        self.altura = 6000  # metros
        self.caracteristicas = ["Montaña sagrada", "Zona de Cusco", "Peregrinación"]

class ApuHualcaHualca(ApuBase):
    """Apu Hualca Hualca - Volcán Nevado"""
    def __init__(self):
        super().__init__(
            nombre="Hualca Hualca",
            color=(200, 255, 255),
            health=87,
            bioma="Volcán Nevado",
            gif="Hualca-Hualca.gif"
        )
        self.illas_robadas = ["Calluha"]
        self.altura = 6025  # metros
        self.caracteristicas = ["Volcán nevado", "Zona de Arequipa", "Forma cónica"]

class ApuUarancante(ApuBase):
    """Apu Uarancante - Pico Andino"""
    def __init__(self):
        super().__init__(
            nombre="Uarancante",
            color=(255, 255, 150),
            health=89,
            bioma="Pico Andino",
            gif="Coropuna.gif"
        )
        self.illas_robadas = ["Inti"]
        self.altura = 5800  # metros
        self.caracteristicas = ["Pico andino", "Zona de Puno", "Nevado"]

class ApuAllincapac(ApuBase):
    """Apu Allincapac - Montaña Dorada"""
    def __init__(self):
        super().__init__(
            nombre="Allincapac",
            color=(255, 215, 0),
            health=93,
            bioma="Montaña Dorada",
            gif="Allincapac.gif"
        )
        self.illas_robadas = ["Killa"]
        self.altura = 5900  # metros
        self.caracteristicas = ["Montaña dorada", "Zona de Apurímac", "Sagrada"]

class ApuKatunqui(ApuBase):
    """Apu Katunqui - Volcán Inactivo"""
    def __init__(self):
        super().__init__(
            nombre="Katunqui",
            color=(200, 100, 255),
            health=85,
            bioma="Volcán Inactivo",
            gif="Katunqui.gif"
        )
        self.illas_robadas = ["Chaska"]
        self.altura = 5700  # metros
        self.caracteristicas = ["Volcán inactivo", "Zona de Moquegua", "Forma redondeada"]

class ApuPatallacta(ApuBase):
    """Apu Patallacta - Ruinas Sagradas"""
    def __init__(self):
        super().__init__(
            nombre="Patallacta",
            color=(139, 69, 19),
            health=100,
            bioma="Ruinas Sagradas",
            gif="Patallacta.gif"
        )
        self.illas_robadas = ["Qullqi", "Quispe"]
        self.altura = 2800  # metros
        self.caracteristicas = ["Ruinas sagradas", "Zona de Cusco", "Sitio arqueológico"]

# ================== DATOS DEL JUEGO (COMPATIBILIDAD) ==================
APUS_DATA = {
    "Huascarán": ApuHuascaran().get_datos(),
    "Coropuna": ApuCoropuna().get_datos(),
    "Misti": ApuMisti().get_datos(),
    "Ampato": ApuAmpato().get_datos(),
    "Sara Sara": ApuSaraSara().get_datos(),
    "Salkantay": ApuSalkantay().get_datos(),
    "Chachani": ApuChachani().get_datos(),
    "Ccarhuarazo": ApuCcarhuarazo().get_datos(),
    "Rasuwillka": ApuRasuwillka().get_datos(),
    "Hualca Hualca": ApuHualcaHualca().get_datos(),
    "Uarancante": ApuUarancante().get_datos(),
    "Allincapac": ApuAllincapac().get_datos(),
    "Katunqui": ApuKatunqui().get_datos(),
    "Patallacta": ApuPatallacta().get_datos()
}

# GIFs de fondo para cada escena/bioma (rutas actualizadas)
BIOMA_GIFS = [
    "biomas/primerBio.gif",                 # Huascarán
    "biomas/lluvia.gif",                    # Coropuna
    "biomas/segundoBio.gif",                # Misti
    "biomas/primerBio.gif",                 # Ampato (reutilizado)
    "biomas/segundoBio.gif",                # Sara Sara (reutilizado)
    "biomas/selva.gif",                     # Salkantay
    "biomas/lluvia.gif",                    # Chachani (reutilizado)
    "biomas/Fondo_glaciar.gif",             # Ccarhuarazo
    "biomas/primerBio.gif",                 # Rasuwillka (reutilizado)
    "biomas/segundoBio.gif",                # Hualca Hualca (reutilizado)
    "biomas/lluvia.gif",                    # Uarancante (reutilizado)
    "biomas/Fondo_glaciar.gif",             # Allincapac (reutilizado)
    "biomas/selva.gif",                     # Katunqui (reutilizado)
    "biomas/primerBio.gif"                  # Patallacta (reutilizado)
]

# Música para cada bioma (rutas actualizadas)
BIOMA_MUSIC = [
    "music/Nevado1.mp3",          # Huascarán
    "music/Musica3.mp3",          # Coropuna
    "music/It's Showtime!.mp3",   # Misti
    "music/Música_4.mp3",         # Ampato
    "music/Música_5.mp3",         # Sara Sara
    "music/Invierno_2.mp3",       # Salkantay
    "music/Determination.mp3",    # Chachani
    "music/Musica3.mp3",          # Ccarhuarazo (reutilizado)
    "music/Nevado1.mp3",          # Rasuwillka (reutilizado)
    "music/Música_4.mp3",         # Hualca Hualca (reutilizado)
    "music/Música_5.mp3",         # Uarancante (reutilizado)
    "music/Invierno_2.mp3",       # Allincapac (reutilizado)
    "music/Determination.mp3",    # Katunqui (reutilizado)
    "music/Last Goodbye(End Music).mp3"  # Patallacta
]

# ================== ARRAYS/LISTAS DONDE SE GUARDAN LAS ILLAS ==================
# 📦 ILLAS_ROBADAS_POR_ESCENA: Array principal donde se guardan las illas por escena
# 📦 ILLAS_GIFS: Diccionario que mapea cada illa con su archivo GIF
# 📦 player.articulos_collected: Lista donde se guardan las illas recolectadas por el jugador

# Illas robadas divididas entre los 14 Apus (19 artículos total)
ILLAS_ROBADAS_POR_ESCENA = [
    # Escena 1 - Huascarán (2 illas)
    ["Tumi", "Chacana"],
    # Escena 2 - Coropuna (2 illas)
    ["Perro Viringo", "Cuy"],
    # Escena 3 - Misti (2 illas)  
    ["Illa", "Torito"],
    # Escena 4 - Ampato (2 illas)
    ["Qullqi", "Quispe"],
    # Escena 5 - Sara Sara (2 illas)
    ["Papa", "Maíz"],
    # Escena 6 - Salkantay (1 illa)
    ["Huashacara"],
    # Escena 7 - Chachani (2 illas)
    ["Qori", "Chuño"],
    # Escena 8 - Ccarhuarazo (1 illa)
    ["Cungalpo"],
    # Escena 9 - Rasuwillka (1 illa)
    ["Hizanche"],
    # Escena 10 - Hualca Hualca (1 illa)
    ["Calluha"],
    # Escena 11 - Uarancante (1 illa)
    ["Inti"],
    # Escena 12 - Allincapac (1 illa)
    ["Killa"],
    # Escena 13 - Katunqui (1 illa)
    ["Chaska"],
    # Escena 14 - Patallacta (1 illa)
    ["Tumi"]
]

# GIFs para cada illa robada (rutas actualizadas)
ILLAS_GIFS = {
    "Tumi": "illas/Tumi.gif",   
    "Chacana": "illas/Chacana.gif", 
    "Illa": "illas/Illa.gif",
    "Torito": "illas/Torito.gif",
    "Perro Viringo": "illas/Perro Viringo.gif",
    "Cuy": "illas/Cuy.gif",
    "Qullqi": "illas/Qullqi.gif",
    "Quispe": "illas/Quispe.gif",
    "Qori": "illas/Qori.gif",
    "Chuño": "illas/Chuño.gif",
    "Papa": "illas/papa.gif",
    "Maíz": "illas/Maíz.gif",
    "Calluha": "illas/Calluna.gif",
    "Cungalpo": "illas/Cungalpo.gif",
    "Hizanche": "illas/Hizanche.gif",
    "Huashacara": "illas/Huashacara.gif",
    "Inti": "illas/inti.gif",
    "Killa": "illas/Killa.gif",
    "Chaska": "illas/Chaska.gif"
}

# ================== CARGA DE PREGUNTAS DESDE JSON ==================
import json

def cargar_preguntas_desde_json():
    """Carga las preguntas desde el archivo preguntas.json"""
    try:
        with open("preguntas.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            preguntas = datos["preguntas"]
            print(f"✅ Cargadas {len(preguntas)} preguntas desde preguntas.json")
            return preguntas
    except FileNotFoundError:
        print("❌ Archivo preguntas.json no encontrado, usando preguntas por defecto")
        return preguntas_por_defecto()
    except Exception as e:
        print(f"❌ Error cargando preguntas.json: {e}, usando preguntas por defecto")
        return preguntas_por_defecto()

def preguntas_por_defecto():
    """Preguntas por defecto en caso de error"""
    return [
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
        }
    ]

# Cargar preguntas al inicio
PREGUNTAS_APUS = cargar_preguntas_desde_json()

# Crear diccionario de preguntas por nombre de Apu para acceso rápido
PREGUNTAS_POR_APU = {}
for pregunta in PREGUNTAS_APUS:
    PREGUNTAS_POR_APU[pregunta["apu"]] = pregunta

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
        
# ================== MENÚ E INSTRUCCIONES ==================
# Las clases MainMenu e InstructionsScreen ahora están en menu.py
# para mantener el código más organizado y modular


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
        
        # Sistema de recolección por proximidad
        self.collection_radius = 60  # Radio para recolectar illas
        self.mochila = MochilaVisual()  # Mochila visual

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
        """🎮 BOTONES PARA MOVER AL PERSONAJE EKEKO:
        - A: Mover hacia la izquierda
        - D: Mover hacia la derecha
        - W: Saltar
        - J: Ver/Ocultar mochila (manejado en GameManager)
        - ↑↓: Navegar en preguntas (en QuestionScreen)
        - ENTER: Confirmar respuesta (en QuestionScreen)
        """
        self.vel_x = 0
        self.walking = False
        if keys[pygame.K_a]:  # 🎮 BOTÓN IZQUIERDA
            self.vel_x = -self.speed
            self.facing_right = False
            self.walking = True
        elif keys[pygame.K_d]:  # 🎮 BOTÓN DERECHA
            self.vel_x = self.speed
            self.facing_right = True
            self.walking = True
        if keys[pygame.K_w] and self.on_ground:  # 🎮 BOTÓN SALTO
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
                self.mochila.agregar_illa(articulo)  # Agregar a la mochila visual
                # Reproducir sonido de masticación
                self.play_chew_sound()
                print(f"🎒 Ekeko recolectó: {articulo}")
    
    def play_chew_sound(self):
        """Reproduce un sonido de masticación"""
        try:
            # Crear un sonido simple de masticación usando pygame sin numpy
            sample_rate = 22050
            duration = 0.08  # Más corto para mejor rendimiento
            samples = int(sample_rate * duration)
            
            # Generar un sonido tipo "masticación" usando array simple
            import array
            # Crear array mono primero
            sound_array_mono = array.array('h')
            
            for i in range(samples):
                # Crear un sonido tipo "crunch" con múltiples frecuencias
                t = float(i) / sample_rate
                wave = int(32767 * 0.15 * (
                    math.sin(2 * math.pi * 200 * t) +
                    0.5 * math.sin(2 * math.pi * 400 * t) +
                    0.25 * math.sin(2 * math.pi * 600 * t)
                ) * math.exp(-t * 10))
                wave = max(-32767, min(32767, wave))  # Limitar valores
                sound_array_mono.append(wave)
            
            # Convertir a estéreo duplicando el canal
            sound_array_stereo = array.array('h')
            for sample in sound_array_mono:
                sound_array_stereo.append(sample)  # Canal izquierdo
                sound_array_stereo.append(sample)  # Canal derecho
            
            sound = pygame.sndarray.make_sound(sound_array_stereo)
            sound.set_volume(0.2)
            sound.play()
        except Exception:
            # Si falla, simplemente no reproducir sonido (silenciosamente)
            pass
    
    def check_collection_proximity(self, articulos_list):
        """Verificar si el jugador está cerca de alguna illa para recolectarla"""
        for articulo in articulos_list:
            if not articulo.collected:
                # Calcular distancia entre el jugador y la illa
                distance = math.sqrt((self.rect.centerx - articulo.rect.centerx)**2 + 
                                  (self.rect.centery - articulo.rect.centery)**2)
                
                if distance <= self.collection_radius:
                    # Recolectar la illa
                    articulo.collected = True
                    self.collect_articulos([articulo.name])
                    return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text_surface = self.font.render("Ekeko", True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(text_surface, text_rect)
        
        # Dibujar la mochila
        self.mochila.draw(screen)


class Apu:
    def __init__(self, name, x, y, scene_number=0, arbol_apus=None):
        self.name = name
        # Usar el árbol binario para obtener los datos del Apu
        if arbol_apus:
            self.data = arbol_apus.obtener_datos_apu(name)
            if not self.data:
                print(f"Error: No se encontró el Apu {name} en el árbol")
                self.data = {"color": (128, 128, 128), "health": 50, "bioma": "Desconocido", "gif": "coropuna.gif"}
        else:
            # Fallback a APUS_DATA si no se proporciona el árbol
            self.data = APUS_DATA[name]
        # Tamaño de Apu: doble del tamaño de Ekeko
        # Ekeko tiene scale_factor=0.1, así que su tamaño base es 40*0.1 = 4, altura 60*0.1 = 6
        # Apu será el doble: 80x120
        self.size = 160  # Doble del tamaño original (80 -> 160)
        self.health = self.data["health"]
        self.max_health = self.data["health"]
        self.scene_number = scene_number

        apu_gif_path = f"apus/{self.data['gif']}"
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
        self.facing_right = True  # Dirección inicial del Apu

    def update(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.original_frames)
            # Voltear el sprite según la dirección
            if not self.facing_right:
                self.image = pygame.transform.flip(self.original_frames[self.frame_index], True, False)
            else:
                self.image = self.original_frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text_surface = self.font.render(f"Apu {self.name}", True, WHITE)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 25))
        screen.blit(text_surface, text_rect)

    def give_illas_to_player(self, player, scene_number):
        """El Apu muestra las illas robadas - el jugador debe recogerlas por radio"""
        illas = ILLAS_ROBADAS_POR_ESCENA[scene_number]
        message = f"🎁 Apu {self.name} ha liberado las illas sagradas: "
        
        for illa in illas:
            message += f"{illa}, "
        
        message = message.rstrip(", ") + " ¡Acércate para recolectarlas!"
        print(message)
        return illas


class Portal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.is_open = False
        self.animation_timer = 0
        self.rotation_angle = 0
        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def open_portal(self):
        self.is_open = True

    def update(self):
        if self.is_open:
            self.animation_timer += 0.08  # Más lento para mejor rendimiento
            self.rotation_angle += 1.5  # Rotación más lenta
            if self.rotation_angle >= 360:
                self.rotation_angle = 0

    def draw(self, screen):
        center_x = self.rect.centerx
        center_y = self.rect.centery
        radius = self.rect.width // 2
        
        if not self.is_open:
            # Portal cerrado - dibujar como un hueco oscuro pixelado
            pygame.draw.circle(screen, (20, 20, 40), (center_x, center_y), radius)
            pygame.draw.circle(screen, BLACK, (center_x, center_y), radius - 5)
            pygame.draw.circle(screen, (40, 40, 60), (center_x, center_y), radius - 10, 2)
        else:
            # Portal abierto - galaxia pixelada pequeña
            # Estrellas/puntos brillantes giratorios (efecto galaxia)
            num_stars = 15  # Menos estrellas para mejor rendimiento
            for i in range(num_stars):
                angle = (360 / num_stars) * i + self.rotation_angle
                distance = radius * (0.3 + 0.7 * ((i % 3) / 3))
                star_x = center_x + int(distance * math.cos(math.radians(angle)))
                star_y = center_y + int(distance * math.sin(math.radians(angle)))
                
                # Dibujar estrellas pixeladas (asegurar valores válidos 0-255)
                brightness = int(100 + 155 * abs(math.sin(self.animation_timer + i)))
                brightness = max(0, min(255, brightness))  # Limitar entre 0 y 255
                star_r = max(0, min(255, brightness // 3))
                star_g = max(0, min(255, brightness // 2))
                star_b = max(0, min(255, brightness))
                star_color = (star_r, star_g, star_b)
                pygame.draw.rect(screen, star_color, (star_x - 1, star_y - 1, 3, 3))
            
            # Núcleo central tipo galaxia (espiral pixelada)
            inner_radius = int(radius * 0.5)
            for r in range(inner_radius, 0, -4):  # Menos círculos para mejor rendimiento
                alpha = int(200 * (r / inner_radius))
                alpha = max(0, min(255, alpha))  # Limitar entre 0 y 255
                # Colores morados/azules tipo galaxia
                color_r = max(0, min(255, alpha // 4))
                color_g = max(0, min(255, alpha // 3))
                color_b = max(0, min(255, alpha))
                color = (color_r, color_g, color_b)
                pygame.draw.circle(screen, color, (center_x, center_y), r)
            
            # Espirales exteriores pixeladas
            for spiral in range(2):
                for i in range(0, 360, 20):  # Menos puntos para mejor rendimiento
                    angle = math.radians(i + self.rotation_angle + spiral * 180)
                    spiral_radius = radius * 0.6 + (radius * 0.4) * (i / 360)
                    px = center_x + int(spiral_radius * math.cos(angle))
                    py = center_y + int(spiral_radius * math.sin(angle))
                    intensity = int(150 + 105 * abs(math.sin(self.animation_timer + i)))
                    intensity = max(0, min(255, intensity))  # Limitar entre 0 y 255
                    pixel_r = max(0, min(255, intensity // 4))
                    pixel_g = max(0, min(255, intensity // 3))
                    pixel_b = max(0, min(255, intensity))
                    pixel_color = (pixel_r, pixel_g, pixel_b)
                    pygame.draw.rect(screen, pixel_color, (px - 1, py - 1, 2, 2))
            
            # Borde pixelado giratorio
            for i in range(0, 360, 20):
                angle_rad = math.radians(i + self.rotation_angle * 2)
                edge_x = center_x + int(radius * math.cos(angle_rad))
                edge_y = center_y + int(radius * math.sin(angle_rad))
                edge_color = (100, 150, 255)
                pygame.draw.rect(screen, edge_color, (edge_x - 2, edge_y - 2, 4, 4))
            
            # Texto indicativo
            text_surface = self.font.render("¡Portal Abierto!", True, GREEN)
            text_rect = text_surface.get_rect(center=(center_x, self.rect.bottom + 20))
            screen.blit(text_surface, text_rect)
            hint_text = pygame.font.SysFont("Arial", 12).render("Cae dentro para continuar", True, YELLOW)
            hint_rect = hint_text.get_rect(center=(center_x, self.rect.bottom + 40))
            screen.blit(hint_text, hint_rect)


class Articulo:
    def __init__(self, name, x, y):
        self.name = name
        # Aumentar el tamaño de las illas
        self.size = 50  # Aumentado de 30 a 50
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.collected = False
        self.color = (255, 255, 0)
        self.float_timer = 0
        self.base_y = y
        self.base_x = x
        self.font = pygame.font.SysFont("Arial", 14, bold=True)  # Fuente más grande
        
        # Variables para animación de giro y movimiento
        self.rotation_angle = 0
        self.rotation_speed = 2  # Velocidad de giro
        self.move_radius = 15  # Radio de movimiento circular
        self.move_speed = 0.05  # Velocidad de movimiento circular
        self.move_timer = 0
        
        self.frames = None
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        if name in ILLAS_GIFS:
            gif_path = ILLAS_GIFS[name]
            if os.path.exists(gif_path):
                self.frames = load_gif_frames(gif_path)
                if self.frames:
                    # Aumentar el tamaño de los frames
                    self.frames = [pygame.transform.scale(f, (self.size, self.size)) for f in self.frames]

    def update(self):
        if not self.collected:
            # Animación de flotación vertical
            self.float_timer += 0.1
            self.rect.y = self.base_y + int(8 * math.cos(self.float_timer))
            
            # Animación de movimiento circular
            self.move_timer += self.move_speed
            self.rect.x = self.base_x + int(self.move_radius * math.sin(self.move_timer))
            
            # Animación de giro
            self.rotation_angle += self.rotation_speed
            if self.rotation_angle >= 360:
                self.rotation_angle = 0
            
            # Animación de frames del GIF
            if self.frames:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        if not self.collected:
            if self.frames:
                # Aplicar rotación al frame actual
                rotated_frame = pygame.transform.rotate(self.frames[self.current_frame], self.rotation_angle)
                frame_rect = rotated_frame.get_rect(center=self.rect.center)
                screen.blit(rotated_frame, frame_rect)
            else:
                # Dibujar círculo con rotación visual
                pygame.draw.circle(screen, self.color, self.rect.center, self.size // 2)
                pygame.draw.circle(screen, WHITE, self.rect.center, self.size // 2, 3)
                
                # Dibujar efecto de giro con líneas
                center_x, center_y = self.rect.center
                for i in range(0, 360, 45):
                    angle_rad = math.radians(i + self.rotation_angle)
                    end_x = center_x + int((self.size // 3) * math.cos(angle_rad))
                    end_y = center_y + int((self.size // 3) * math.sin(angle_rad))
                    pygame.draw.line(screen, WHITE, (center_x, center_y), (end_x, end_y), 2)
            
            # Texto con sombra para mejor visibilidad
            text_surface = self.font.render(self.name, True, WHITE)
            text_shadow = self.font.render(self.name, True, BLACK)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 15))
            shadow_rect = text_shadow.get_rect(center=(self.rect.centerx + 1, self.rect.bottom + 16))
            screen.blit(text_shadow, shadow_rect)
            screen.blit(text_surface, text_rect)

class MochilaVisual:
    """Clase para la mochila visual donde se guardan las illas recolectadas"""
    def __init__(self):
        self.width = 300  # Aumentado para mostrar más illas
        self.height = 400  # Aumentado para mostrar GIFs de illas
        self.x = (SCREEN_WIDTH - self.width) // 2  # Centrado horizontalmente
        self.y = (SCREEN_HEIGHT - self.height) // 2  # Centrado verticalmente
        self.illas_guardadas = []
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 12)
        
        # Estado de mostrar/ocultar mochila
        self.mostrar_mochila = False
        
        # Cargar GIF de la mochila si existe
        self.mochila_gif = None
        mochila_path = "mochila.gif"  # Ruta actualizada
        if os.path.exists(mochila_path):
            self.mochila_frames = load_gif_frames(mochila_path)
            if self.mochila_frames:
                self.mochila_frames = [pygame.transform.scale(f, (self.width, self.height)) for f in self.mochila_frames]
                self.current_frame = 0
                self.animation_timer = 0
                self.animation_speed = 0.1
                self.mochila_gif = True
            else:
                self.mochila_gif = False
        else:
            self.mochila_gif = False
        
        # Cache de GIFs de illas para mostrar en la mochila
        self.illas_gifs_cache = {}
    
    def agregar_illa(self, illa_name):
        """Agregar una illa a la mochila"""
        if illa_name not in self.illas_guardadas:
            self.illas_guardadas.append(illa_name)
            # Cargar GIF de la illa si no está en cache
            self._cargar_gif_illa(illa_name)
            print(f"🎒 Illa {illa_name} guardada en la mochila!")
    
    def _cargar_gif_illa(self, illa_name):
        """Cargar el GIF de una illa específica"""
        if illa_name not in self.illas_gifs_cache:
            if illa_name in ILLAS_GIFS:
                gif_path = ILLAS_GIFS[illa_name]
                if os.path.exists(gif_path):
                    frames = load_gif_frames(gif_path)
                    if frames:
                        # Redimensionar frames para la mochila
                        size_illa = 40  # Tamaño de illa en la mochila
                        frames_resized = [pygame.transform.scale(f, (size_illa, size_illa)) for f in frames]
                        self.illas_gifs_cache[illa_name] = {
                            'frames': frames_resized,
                            'current_frame': 0,
                            'animation_timer': 0,
                            'animation_speed': 0.1
                        }
                        print(f"📁 GIF de {illa_name} cargado para la mochila")
    
    def alternar_visibilidad(self):
        """Alternar entre mostrar y ocultar la mochila"""
        self.mostrar_mochila = not self.mostrar_mochila
        print(f"🎒 Mochila {'abierta' if self.mostrar_mochila else 'cerrada'}")
    
    def update(self):
        """Actualizar animación de la mochila y las illas"""
        if self.mostrar_mochila:
            # Actualizar animación de la mochila
            if self.mochila_gif:
                self.animation_timer += self.animation_speed
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.mochila_frames)
            
            # Actualizar animaciones de las illas
            for illa_name in self.illas_gifs_cache:
                illa_data = self.illas_gifs_cache[illa_name]
                illa_data['animation_timer'] += illa_data['animation_speed']
                if illa_data['animation_timer'] >= 1:
                    illa_data['animation_timer'] = 0
                    illa_data['current_frame'] = (illa_data['current_frame'] + 1) % len(illa_data['frames'])
    
    def draw(self, screen):
        """Dibujar la mochila completa con illas animadas"""
        if not self.mostrar_mochila:
            return
        
        # Crear fondo semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Dibujar fondo de la mochila
        mochila_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (101, 67, 33), mochila_rect)
        pygame.draw.rect(screen, WHITE, mochila_rect, 3)
        
        # Dibujar GIF de la mochila si existe
        if self.mochila_gif:
            screen.blit(self.mochila_frames[self.current_frame], (self.x, self.y))
        
        # Título de la mochila
        title_text = self.font.render("MOCHILA DE EKEKO", True, WHITE)
        title_rect = title_text.get_rect(center=(self.x + self.width // 2, self.y + 20))
        screen.blit(title_text, title_rect)
        
        # Contador de illas
        illas_text = f"Illas Recolectadas: {len(self.illas_guardadas)}/19"
        count_text = self.font_small.render(illas_text, True, YELLOW)
        count_rect = count_text.get_rect(center=(self.x + self.width // 2, self.y + 45))
        screen.blit(count_text, count_rect)
        
        # Dibujar illas con sus GIFs animados
        if self.illas_guardadas:
            start_y = self.y + 70
            illas_por_fila = 4  # 4 illas por fila
            spacing_x = 60
            spacing_y = 60
            
            for i, illa_name in enumerate(self.illas_guardadas):
                fila = i // illas_por_fila
                columna = i % illas_por_fila
                
                x = self.x + 20 + (columna * spacing_x)
                y = start_y + (fila * spacing_y)
                
                # Dibujar GIF de la illa si está en cache
                if illa_name in self.illas_gifs_cache:
                    illa_data = self.illas_gifs_cache[illa_name]
                    current_frame = illa_data['frames'][illa_data['current_frame']]
                    screen.blit(current_frame, (x, y))
                else:
                    # Dibujar círculo como fallback
                    pygame.draw.circle(screen, YELLOW, (x + 20, y + 20), 20)
                    pygame.draw.circle(screen, WHITE, (x + 20, y + 20), 20, 2)
                
                # Dibujar nombre de la illa
                nombre_text = self.font_small.render(illa_name, True, WHITE)
                nombre_rect = nombre_text.get_rect(center=(x + 20, y + 45))
                screen.blit(nombre_text, nombre_rect)
                
                # Si hay muchas illas, mostrar scroll
                if fila >= 4:  # Máximo 4 filas visibles
                    scroll_text = self.font_small.render("...", True, GRAY)
                    scroll_rect = scroll_text.get_rect(center=(self.x + self.width // 2, y + 30))
                    screen.blit(scroll_text, scroll_rect)
                    break
        else:
            # Mensaje cuando no hay illas
            empty_text = self.font_small.render("No hay illas recolectadas", True, GRAY)
            empty_rect = empty_text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(empty_text, empty_rect)
        
        # Instrucciones para cerrar
        close_text = self.font_small.render("Presiona J para cerrar la mochila", True, WHITE)
        close_rect = close_text.get_rect(center=(self.x + self.width // 2, self.y + self.height - 20))
        screen.blit(close_text, close_rect)
            
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
        """🎮 BOTONES PARA NAVEGAR EN LAS PREGUNTAS:
        - ↑↓: Navegar entre opciones de respuesta
        - ENTER: Confirmar respuesta seleccionada
        """
        if not self.answered:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.selected_option > 0:  # 🎮 BOTÓN ARRIBA
                    self.selected_option -= 1
                elif event.key == pygame.K_DOWN and self.selected_option < len(self.pregunta_data["opciones"]) - 1:  # 🎮 BOTÓN ABAJO
                    self.selected_option += 1
                elif event.key == pygame.K_RETURN:  # 🎮 BOTÓN CONFIRMAR
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
    def __init__(self, scene_number, arbol_apus=None):
        self.scene_number = scene_number
        # Obtener el nombre del Apu usando el árbol binario
        if arbol_apus:
            apu_nodo = arbol_apus.obtener_apu_por_indice(scene_number)
            if apu_nodo:
                self.apu_name = apu_nodo.nombre
            else:
                self.apu_name = list(APUS_DATA.keys())[scene_number]  # Fallback
        else:
            self.apu_name = list(APUS_DATA.keys())[scene_number]  # Fallback
        
        self.apu = Apu(self.apu_name, SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 230, scene_number, arbol_apus)
        self.portal = Portal(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 230)
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

    def start_question(self):
        if not self.showing_question and not self.completed:
            # Buscar pregunta por nombre del Apu
            if self.apu_name in PREGUNTAS_POR_APU:
                pregunta_data = PREGUNTAS_POR_APU[self.apu_name]
                self.question_screen = QuestionScreen(pregunta_data)
                self.showing_question = True
            else:
                print(f"⚠️ No se encontró pregunta para el Apu: {self.apu_name}")
                # Usar pregunta por defecto si no se encuentra
                pregunta_data = {
                    "apu": self.apu_name,
                    "pregunta": "¿Cuál fue la capital del Imperio Inca?",
                    "opciones": ["Cusco", "Machu Picchu", "Ollantaytambo", "Sacsayhuamán"],
                    "respuesta_correcta": 0
                }
                self.question_screen = QuestionScreen(pregunta_data)
                self.showing_question = True

    def handle_event(self, event, player):
        if self.showing_question and self.question_screen:
            self.question_screen.handle_input(event)
            
            if self.question_screen.is_finished():
                if self.question_screen.correct:
                    self.completed = True
                    self.portal.open_portal()
                    self.player_can_advance = True
                    
                    # El Apu entrega las illas robadas
                    illas_received = self.apu.give_illas_to_player(player, self.scene_number)
                    self.illas_message = f"¡Recibiste: {', '.join(illas_received)}!"
                    self.illas_message_timer = 300
                    
                    # Mostrar artículos visuales flotando
                    self.show_artikulos()
                    
                else:
                    if player.lose_life():
                        # Buscar pregunta por nombre del Apu
                        if self.apu_name in PREGUNTAS_POR_APU:
                            pregunta_data = PREGUNTAS_POR_APU[self.apu_name]
                            self.question_screen = QuestionScreen(pregunta_data)
                        else:
                            # Usar pregunta por defecto
                            pregunta_data = {
                                "apu": self.apu_name,
                                "pregunta": "¿Cuál fue la capital del Imperio Inca?",
                                "opciones": ["Cusco", "Machu Picchu", "Ollantaytambo", "Sacsayhuamán"],
                                "respuesta_correcta": 0
                            }
                            self.question_screen = QuestionScreen(pregunta_data)
                    else:
                        stop_music()
                        return "GAME_OVER"
                
                self.showing_question = False
        
        return "CONTINUE"

    def update(self, player):
        # Hacer que el Apu mire al ekeko
        if player.rect.centerx < self.apu.rect.centerx:
            self.apu.facing_right = False
        else:
            self.apu.facing_right = True
        
        self.apu.update()
        self.portal.update()
        
        if self.question_screen:
            self.question_screen.update()
        
        # Actualizar artículos visuales
        for articulo in self.artikulos_visuales:
            articulo.update()
        
        # Verificar recolección por proximidad (solo por radio, no automático)
        if self.completed:
            player.check_collection_proximity(self.artikulos_visuales)
        
        if self.illas_message_timer > 0:
            self.illas_message_timer -= 1
        
        if not self.showing_question and not self.completed:
            if self.apu.rect.colliderect(player.rect):
                self.start_question()

    def draw(self, screen, player):
        font = pygame.font.SysFont("Arial", 20, bold=True)
        # Obtener el bioma del Apu usando el árbol binario o fallback
        if hasattr(self, 'apu') and hasattr(self.apu, 'data'):
            bioma = self.apu.data.get('bioma', 'Desconocido')
        else:
            bioma = APUS_DATA.get(self.apu_name, {}).get('bioma', 'Desconocido')
        
        scene_text = font.render(f"Escena {self.scene_number + 1}/14 - {bioma}", True, WHITE)
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
        
        # Dibujar artículos visuales flotantes con animación
        for articulo in self.artikulos_visuales:
            articulo.draw(screen)
            
            # Dibujar indicador de proximidad si está cerca del jugador
            if not articulo.collected:
                distance = math.sqrt((player.rect.centerx - articulo.rect.centerx)**2 + 
                                  (player.rect.centery - articulo.rect.centery)**2)
                if distance <= player.collection_radius:
                    # Dibujar círculo de proximidad
                    pygame.draw.circle(screen, (255, 255, 0), articulo.rect.center, 
                                     player.collection_radius, 2)
                    # Dibujar texto de instrucción
                    collect_text = pygame.font.SysFont("Arial", 12, bold=True).render(
                        "¡Acércate para recolectar!", True, YELLOW)
                    collect_rect = collect_text.get_rect(center=(articulo.rect.centerx, 
                                                               articulo.rect.top - 30))
                    screen.blit(collect_text, collect_rect)
        
        if not self.completed:
            self.apu.draw(screen)
        self.portal.draw(screen)
        
        if self.showing_question and self.question_screen:
            self.question_screen.draw(screen)

    def can_advance(self, player):
        # El jugador cae en el portal para avanzar
        if self.player_can_advance:
            # Verificar si el jugador está dentro del portal (colisión con el círculo)
            portal_center_x = self.portal.rect.centerx
            portal_center_y = self.portal.rect.centery
            portal_radius = self.portal.rect.width // 2
            
            player_center_x = player.rect.centerx
            player_center_y = player.rect.centery
            
            distance = math.sqrt((player_center_x - portal_center_x)**2 + 
                               (player_center_y - portal_center_y)**2)
            
            return distance < portal_radius
        return False


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
        self.total_scenes = 14  # Actualizado a 14 Apus
        self.scenes = []
        self.player = Player(100, SCREEN_HEIGHT - 250, gif_path="ekeko.gif", scale_factor=0.1)
        self.background = AnimatedBackground(scene_number=0)
        self.game_state = "MENU"  # 👉 empieza en menú
        self.font_big = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)

        # ✅ Árbol binario de Apus
        self.arbol_apus = ArbolApus()
        self.poblar_arbol_apus()  # Poblar el árbol con los 14 Apus

        # ✅ Menú principal (usando archivo separado)
        from menu import MainMenu
        self.main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

        # ✅ Escenas (ahora usando el árbol binario)
        for i in range(self.total_scenes):
            self.scenes.append(GameScene(i, self.arbol_apus))

        # ✅ Música
        self.current_music = None
        self.load_menu_music()  # 🎵 suena música del menú apenas inicia



    def poblar_arbol_apus(self):
        """Poblar el árbol binario con los 14 Apus del juego usando clases específicas"""
        print("🌳 Poblando árbol binario con los 14 Apus usando clases específicas...")
        
        # Crear instancias de cada clase de Apu (en orden de la lista de Ekeko)
        apus_instancias = [
            ApuHuascaran(), ApuCoropuna(), ApuMisti(), ApuAmpato(),
            ApuSaraSara(), ApuSalkantay(), ApuChachani(), ApuCcarhuarazo(),
            ApuRasuwillka(), ApuHualcaHualca(), ApuUarancante(), ApuAllincapac(),
            ApuKatunqui(), ApuPatallacta()
        ]
        
        # Insertar todos los Apus en el árbol binario
        for apu in apus_instancias:
            self.arbol_apus.insertar(apu.nombre, apu.get_datos())
            print(f"🏔️ {apu.nombre} ({apu.bioma}) - Altura: {apu.altura}m - Illas: {apu.illas_robadas}")
        
        print(f"✅ Árbol binario poblado con {self.arbol_apus.total_apus} Apus")
        # Mostrar estructura del árbol para debugging
        self.arbol_apus.mostrar_arbol()
        
        # Demostrar funcionalidades del árbol binario
        self.demostrar_funcionalidades_arbol()
    
    def demostrar_funcionalidades_arbol(self):
        """Demuestra las funcionalidades del árbol binario"""
        print("\n=== DEMOSTRACIÓN DE FUNCIONALIDADES DEL ÁRBOL BINARIO ===")
        
        # 1. Buscar un Apu específico
        apu_buscado = self.arbol_apus.buscar("Huascarán")
        if apu_buscado:
            print(f"🔍 Búsqueda exitosa: Encontrado {apu_buscado.nombre} - {apu_buscado.datos['bioma']}")
        else:
            print("❌ Apu no encontrado")
        
        # 2. Recorrer todos los Apus en orden alfabético
        print("\n📋 Recorrido inorden (orden alfabético) de todos los Apus:")
        apus_ordenados = self.arbol_apus.recorrer_inorden()
        for i, apu in enumerate(apus_ordenados):
            print(f"  {i+1}. {apu.nombre} - {apu.datos['bioma']}")
        
        # 3. Obtener Apu por índice
        apu_por_indice = self.arbol_apus.obtener_apu_por_indice(0)
        if apu_por_indice:
            print(f"\n🎯 Primer Apu en orden alfabético: {apu_por_indice.nombre}")
        
        # 4. Mostrar cómo funciona el recorrido por niveles
        print("\n🌳 FUNCIONAMIENTO DEL ÁRBOL BINARIO:")
        print("• ORDENACIÓN: Los Apus se ordenan alfabéticamente")
        print("• INSERCIÓN: Nombres menores van a la IZQUIERDA, mayores a la DERECHA")
        print("• BÚSQUEDA: Compara alfabéticamente y navega por niveles")
        print("• RECORRIDO: Visita izquierda → raíz → derecha (orden alfabético)")
        print("• CAMBIO DE NIVEL: Automático según comparación alfabética")
        
        print("=" * 60)

    # 🔽 LO NUEVO QUE DEBES AGREGAR AQUÍ
    def load_menu_music(self):
        # Intentar varias opciones de música para el menú
        menu_music_options = [
            "music/Determination.mp3",
            "music/It's Showtime!.mp3",
            "music/Nevado1.mp3",
            "music/Musica3.mp3"
        ]
        menu_music_path = None
        for path in menu_music_options:
            if os.path.exists(path):
                menu_music_path = path
                break
        
        if menu_music_path and menu_music_path != self.current_music:
            stop_music()
            play_music(menu_music_path)
            self.current_music = menu_music_path
            print(f"🎵 Música del MENÚ principal cargada: {menu_music_path}")
        else:
            print("🎵 No se encontró música para el menú")


    def load_biome_music(self, scene_number):
        """Carga la música del bioma correspondiente a la escena"""
        if scene_number < len(BIOMA_MUSIC):
            music_path = BIOMA_MUSIC[scene_number]
            if os.path.exists(music_path) and music_path != self.current_music:
                stop_music()
                play_music(music_path)
                self.current_music = music_path
                print(f"🎵 Música del bioma {scene_number+1}: {music_path}")
            elif not os.path.exists(music_path):
                print(f"⚠️ Música no encontrada: {music_path}")
        else:
            print(f"⚠️ Escena {scene_number} fuera de rango para música")

    def handle_event(self, event):
        if self.game_state == "MENU":
            # Manejar tecla ESC para salir
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "QUIT"
            
            menu_result = self.main_menu.handle_input(event)
            if menu_result == "JUGAR":
                stop_music()
                self.restart_game()  # Reiniciar el juego completamente
                self.game_state = "PLAYING"
                self.load_biome_music(0)
            elif menu_result == "INSTRUCCIONES":
                self.game_state = "INSTRUCTIONS"
            elif menu_result == "SALIR":
                return "QUIT"
                
        elif self.game_state == "INSTRUCTIONS":
            if not hasattr(self, 'instructions_screen'):
                from menu import InstructionsScreen
                self.instructions_screen = InstructionsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
            instr_result = self.instructions_screen.handle_input(event)
            if instr_result == "BACK":
                self.game_state = "MENU"
                
        elif self.game_state == "PLAYING":
            # Manejar tecla J para mostrar/ocultar mochila
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                self.player.mochila.alternar_visibilidad()
            
            result = self.scenes[self.current_scene].handle_event(event, self.player)
            if result == "GAME_OVER":
                self.game_state = "GAME_OVER"
                stop_music()
                
        elif self.game_state in ["GAME_OVER", "VICTORY", "CREDITS"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m or event.key == pygame.K_RETURN:
                    stop_music()
                    self.game_state = "MENU"
                    self.load_menu_music()
        
        return "CONTINUE"

    def update(self):
        if self.game_state == "MENU":
            self.main_menu.update()
        elif self.game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            self.player.update()
            
            # Actualizar la mochila del jugador
            self.player.mochila.update()
            
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
        # Reproducir música de final si existe
        end_music = "music/Last Goodbye(End Music).mp3"
        if os.path.exists(end_music):
            play_music(end_music)



    def restart_game(self):
        """Reinicia el juego completamente"""
        self.current_scene = 0
        self.player = Player(100, SCREEN_HEIGHT - 250, gif_path="ekeko.gif", scale_factor=0.1)
        self.background = AnimatedBackground(scene_number=0)
        
        # Recrear las escenas usando el árbol binario
        self.scenes = []
        for i in range(self.total_scenes):
            self.scenes.append(GameScene(i, self.arbol_apus))

    def draw(self, screen):
        if self.game_state == "MENU":
            self.main_menu.draw(screen)
            
        elif self.game_state == "INSTRUCTIONS":
            self.main_menu.draw(screen)  # Fondo del menú
            from menu import InstructionsScreen
            if not hasattr(self, 'instructions_screen'):
                self.instructions_screen = InstructionsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.instructions_screen.draw(screen)
            
        elif self.game_state == "PLAYING":
            self.background.draw(screen)
            self.player.draw(screen)
            self.scenes[self.current_scene].draw(screen, self.player)
            
            # Dibujar mochila si está abierta
            self.player.mochila.draw(screen)
            
            progress_text = self.font_medium.render(f"Progreso: {self.current_scene + 1}/14", True, WHITE)
            screen.blit(progress_text, (SCREEN_WIDTH - 200, 10))
            
        elif self.game_state == "GAME_OVER":
            self.draw_game_over(screen)
            
        elif self.game_state == "VICTORY":
            self.draw_victory(screen)
    
    def draw_credits(self, screen, y_start):
        """Dibuja los créditos del juego"""
        font_credits_title = pygame.font.SysFont("Arial", 24, bold=True)
        font_credits = pygame.font.SysFont("Arial", 18)
        font_credits_small = pygame.font.SysFont("Arial", 16)
        
        y = y_start
        
        # Título de créditos
        credits_title = font_credits_title.render("CRÉDITOS", True, YELLOW)
        credits_title_rect = credits_title.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(credits_title, credits_title_rect)
        y += 50
        
        # Créditos del equipo
        credits_list = [
            ("Noel Jeferson Vilca Quispe", "Programador"),
            ("Paul Anampa", "Diseñador"),
            ("Anderson Rosas", "Efectos especiales"),
            ("Anthony Mondalvo", "Organizador"),
            ("Profesora Norma Leon", "Gracias")
        ]
        
        for name, role in credits_list:
            name_text = font_credits.render(name, True, WHITE)
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(name_text, name_rect)
            y += 25
            
            role_text = font_credits_small.render(role, True, GRAY)
            role_rect = role_text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(role_text, role_rect)
            y += 30
        
        return y
    
    def draw_game_over(self, screen):
        """Dibuja la pantalla de game over con créditos"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_big.render("¡GAME OVER!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Llegaste hasta la escena {self.current_scene + 1}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 130))
        screen.blit(score_text, score_rect)
        
        articles_text = self.font_medium.render(f"Illas recuperadas: {len(self.player.articulos_collected)}/19", True, WHITE)
        articles_rect = articles_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(articles_text, articles_rect)
        
        # Dibujar créditos
        y_credits = self.draw_credits(screen, 220)
        
        # Botón de menú
        menu_text = self.font_medium.render("Presiona 'M' o ENTER para ir al menú", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, y_credits + 20))
        screen.blit(menu_text, menu_rect)
    
    def draw_victory(self, screen):
        """Dibuja la pantalla de victoria con créditos"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        victory_text = self.font_big.render("¡VICTORIA TOTAL!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(victory_text, victory_rect)
        
        completion_text = self.font_medium.render("¡Ekeko completó su aventura por los 14 Apus!", True, WHITE)
        completion_rect = completion_text.get_rect(center=(SCREEN_WIDTH // 2, 130))
        screen.blit(completion_text, completion_rect)
        
        articles_text = self.font_medium.render(
            f"Illas sagradas recuperadas: {len(self.player.articulos_collected)}/19", 
            True, YELLOW
        )
        articles_rect = articles_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(articles_text, articles_rect)
        
        # Dibujar créditos
        y_credits = self.draw_credits(screen, 220)
        
        # Botón de menú
        menu_text = self.font_medium.render("Presiona 'M' o ENTER para ir al menú", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, y_credits + 20))
        screen.blit(menu_text, menu_rect)
    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    result = self.handle_event(event)
                    if result == "QUIT":
                        running = False

            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()
        sys.exit()
def main():
    game = GameManager()
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                result = game.handle_event(event)
                if result == "QUIT":
                    running = False

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()