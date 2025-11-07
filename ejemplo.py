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
    """Representa un nodo del árbol binario que contiene información de un Apu.

    Attributes:
        nombre (str): Nombre del Apu.
        datos (dict): Diccionario con la información del Apu (color, salud, bioma, gif).
        izquierda (NodoApu): Referencia al hijo izquierdo.
        derecha (NodoApu): Referencia al hijo derecho.
    """
    def __init__(self, nombre, datos):
        self.nombre = nombre
        self.datos = datos
        self.izquierda = None
        self.derecha = None


class ArbolApus:
    """Estructura de árbol binario que gestiona los Apus del juego.

    El árbol organiza los Apus alfabéticamente por nombre.
    Se puede insertar, buscar y recorrer para acceder a los datos de cada Apu.
    """

    def __init__(self):
        """Inicializa un árbol binario vacío."""
        self.raiz = None
        self.total_apus = 0

    def insertar(self, nombre, datos):
        """Inserta un nuevo Apu en el árbol binario.

        Si el árbol está vacío, el Apu se convierte en la raíz.  
        Los Apus se ordenan alfabéticamente por su nombre.

        Args:
            nombre (str): Nombre del Apu.
            datos (dict): Diccionario con la información del Apu.
        """
        if self.raiz is None:
            self.raiz = NodoApu(nombre, datos)
            self.total_apus += 1
            print(f"🌳 Insertando {nombre} como RAÍZ del árbol")
        else:
            self._insertar_recursivo(self.raiz, nombre, datos)

    def _insertar_recursivo(self, nodo, nombre, datos):
        """Inserta recursivamente un nuevo nodo en el árbol.

        Args:
            nodo (NodoApu): Nodo actual desde el cual se realiza la comparación.
            nombre (str): Nombre del Apu a insertar.
            datos (dict): Información del Apu.
        """
        if nombre < nodo.nombre:
            if nodo.izquierda is None:
                nodo.izquierda = NodoApu(nombre, datos)
                self.total_apus += 1
                print(f"🌳 Insertando {nombre} a la IZQUIERDA de {nodo.nombre}")
            else:
                self._insertar_recursivo(nodo.izquierda, nombre, datos)
        elif nombre > nodo.nombre:
            if nodo.derecha is None:
                nodo.derecha = NodoApu(nombre, datos)
                self.total_apus += 1
                print(f"🌳 Insertando {nombre} a la DERECHA de {nodo.nombre}")
            else:
                self._insertar_recursivo(nodo.derecha, nombre, datos)

    def buscar(self, nombre):
        """Busca un Apu por su nombre.

        Args:
            nombre (str): Nombre del Apu a buscar.

        Returns:
            NodoApu | None: El nodo que contiene al Apu, o None si no existe.
        """
        return self._buscar_recursivo(self.raiz, nombre)

    def _buscar_recursivo(self, nodo, nombre):
        """Busca recursivamente un Apu en el árbol.

        Args:
            nodo (NodoApu): Nodo actual desde el cual se busca.
            nombre (str): Nombre del Apu.

        Returns:
            NodoApu | None: El nodo encontrado, o None si no existe.
        """
        if nodo is None:
            return None
        if nodo.nombre == nombre:
            return nodo
        elif nombre < nodo.nombre:
            return self._buscar_recursivo(nodo.izquierda, nombre)
        else:
            return self._buscar_recursivo(nodo.derecha, nombre)

    def recorrer_inorden(self):
        """Recorre el árbol en orden alfabético (izquierda → raíz → derecha).

        Returns:
            list[NodoApu]: Lista de los nodos del árbol en orden alfabético.
        """
        apus_ordenados = []
        self._inorden_recursivo(self.raiz, apus_ordenados)
        return apus_ordenados

    def _inorden_recursivo(self, nodo, lista):
        """Recorrido inorden recursivo del árbol.

        Args:
            nodo (NodoApu): Nodo actual.
            lista (list): Lista acumuladora de nodos visitados.
        """
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierda, lista)
            lista.append(nodo)
            self._inorden_recursivo(nodo.derecha, lista)

    def obtener_apu_por_indice(self, indice):
        """Obtiene un Apu según su posición en el recorrido inorden.

        Args:
            indice (int): Posición del Apu en la lista ordenada.

        Returns:
            NodoApu | None: Nodo correspondiente al índice, o None si no existe.
        """
        apus_ordenados = self.recorrer_inorden()
        if 0 <= indice < len(apus_ordenados):
            return apus_ordenados[indice]
        return None

    def obtener_datos_apu(self, nombre):
        """Obtiene los datos de un Apu por su nombre.

        Args:
            nombre (str): Nombre del Apu.

        Returns:
            dict | None: Diccionario con los datos del Apu, o None si no se encuentra.
        """
        nodo = self.buscar(nombre)
        if nodo:
            return nodo.datos
        return None

    def mostrar_arbol(self):
        """Muestra en consola la estructura completa del árbol."""
        print("=== ÁRBOL BINARIO DE APUS ===")
        self._mostrar_recursivo(self.raiz, 0)
        print(f"Total de Apus: {self.total_apus}")

    def _mostrar_recursivo(self, nodo, nivel):
        """Muestra recursivamente la estructura jerárquica del árbol.

        Args:
            nodo (NodoApu): Nodo actual.
            nivel (int): Nivel de profundidad del nodo.
        """
        if nodo is not None:
            self._mostrar_recursivo(nodo.derecha, nivel + 1)
            print("  " * nivel + f"├─ {nodo.nombre} ({nodo.datos['bioma']})")
            self._mostrar_recursivo(nodo.izquierda, nivel + 1)


# ================== CLASES ESPECÍFICAS PARA CADA APU CON SU BIOMA ==================

class ApuBase:
    """Clase base que define la estructura general de un Apu.

    Attributes:
        nombre (str): Nombre del Apu.
        color (tuple[int, int, int]): Color representativo del Apu en formato RGB.
        health (int): Nivel de salud o energía del Apu.
        bioma (str): Tipo de bioma o entorno natural del Apu.
        gif (str): Ruta del archivo gráfico o animación del Apu.
        illas_robadas (list[str]): Lista de ítems o reliquias robadas por el Apu.
    """

    def __init__(self, nombre, color, health, bioma, gif):
        """Inicializa un Apu con sus atributos principales.

        Args:
            nombre (str): Nombre del Apu.
            color (tuple[int, int, int]): Color representativo (RGB).
            health (int): Nivel de energía o salud del Apu.
            bioma (str): Bioma donde habita el Apu.
            gif (str): Nombre del archivo GIF o imagen asociada al Apu.
        """
        self.nombre = nombre
        self.color = color
        self.health = health
        self.bioma = bioma
        self.gif = gif
        self.illas_robadas = []

    def get_datos(self):
        """Retorna los datos del Apu en formato compatible con el árbol binario.

        Returns:
            dict: Contiene el color, salud, bioma y gif del Apu.
        """
        return {
            "color": self.color,
            "health": self.health,
            "bioma": self.bioma,
            "gif": self.gif
        }


# ---------------------- SUBCLASES DE APUS ----------------------

class ApuHuascaran(ApuBase):
    """Representa al Apu Huascarán, ubicado en la Montaña Nevada."""
    def __init__(self):
        super().__init__(
            nombre="Huascarán",
            color=(255, 255, 255),
            health=100,
            bioma="Montaña Nevada",
            gif="Huascaran.gif"
        )
        self.illas_robadas = ["Tumi", "Chacana"]
        self.altura = 6768
        self.caracteristicas = [
            "Pico más alto del Perú",
            "Nevado permanente",
            "Parque Nacional"
        ]


class ApuCoropuna(ApuBase):
    """Representa al Apu Coropuna, un glaciar andino del sur del Perú."""
    def __init__(self):
        super().__init__(
            nombre="Coropuna",
            color=(200, 200, 255),
            health=90,
            bioma="Glaciar",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Perro Viringo", "Cuy"]
        self.altura = 6425
        self.caracteristicas = [
            "Volcán extinto",
            "Glaciar extenso",
            "Reserva natural"
        ]


class ApuMisti(ApuBase):
    """Representa al Apu Misti, un volcán activo cerca de Arequipa."""
    def __init__(self):
        super().__init__(
            nombre="Misti",
            color=(255, 150, 150),
            health=85,
            bioma="Volcán",
            gif="Misti.png"
        )
        self.illas_robadas = ["Illa", "Torito"]
        self.altura = 5822
        self.caracteristicas = [
            "Volcán activo",
            "Cerca de Arequipa",
            "Forma cónica perfecta"
        ]


class ApuAmpato(ApuBase):
    """Representa al Apu Ampato, un volcán del altiplano peruano."""
    def __init__(self):
        super().__init__(
            nombre="Ampato",
            color=(150, 255, 150),
            health=95,
            bioma="Altiplano",
            gif="Ampato.png"
        )
        self.illas_robadas = ["Qullqi", "Quispe"]
        self.altura = 6288
        self.caracteristicas = [
            "Volcán inactivo",
            "Zona de altiplano",
            "Clima frío"
        ]


class ApuSaraSara(ApuBase):
    """Representa al Apu Sara Sara, un volcán andino de Ayacucho."""
    def __init__(self):
        super().__init__(
            nombre="Sara Sara",
            color=(255, 100, 100),
            health=88,
            bioma="Volcán Andino",
            gif="SaraSara.png"
        )
        self.illas_robadas = ["Papa", "Maíz"]
        self.altura = 5505
        self.caracteristicas = [
            "Volcán andino",
            "Zona de Ayacucho",
            "Forma cónica"
        ]


class ApuSalkantay(ApuBase):
    """Representa al Apu Salkantay, ubicado en la Selva Alta."""
    def __init__(self):
        super().__init__(
            nombre="Salkantay",
            color=(100, 255, 200),
            health=90,
            bioma="Selva Alta",
            gif="Salkantay.png"
        )
        self.illas_robadas = ["Huashacara"]
        self.altura = 6271
        self.caracteristicas = [
            "Transición a selva",
            "Biodiversidad única",
            "Camino a Machu Picchu"
        ]


class ApuChachani(ApuBase):
    """Representa al Apu Chachani, un volcán del desierto alto arequipeño."""
    def __init__(self):
        super().__init__(
            nombre="Chachani",
            color=(255, 200, 100),
            health=80,
            bioma="Desierto Alto",
            gif="Chachani.png"
        )
        self.illas_robadas = ["Qori", "Chuño"]
        self.altura = 6057
        self.caracteristicas = [
            "Volcán extinto",
            "Desierto de altura",
            "Arena volcánica"
        ]


class ApuCcarhuarazo(ApuBase):
    """Representa al Apu Ccarhuarazo, un nevado de la Cordillera Central."""
    def __init__(self):
        super().__init__(
            nombre="Ccarhuarazo",
            color=(180, 180, 255),
            health=92,
            bioma="Cordillera Central",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Cungalpo"]
        self.altura = 5120
        self.caracteristicas = [
            "Cordillera central",
            "Zona de Huancavelica",
            "Nevado"
        ]


class ApuRasuwillka(ApuBase):
    """Representa al Apu Rasuwillka, una montaña sagrada de Cusco."""
    def __init__(self):
        super().__init__(
            nombre="Rasuwillka",
            color=(255, 180, 255),
            health=95,
            bioma="Montaña Sagrada",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Hizanche"]
        self.altura = 6000
        self.caracteristicas = [
            "Montaña sagrada",
            "Zona de Cusco",
            "Peregrinación"
        ]


class ApuHualcaHualca(ApuBase):
    """Representa al Apu Hualca Hualca, un volcán nevado de Arequipa."""
    def __init__(self):
        super().__init__(
            nombre="Hualca Hualca",
            color=(200, 255, 255),
            health=87,
            bioma="Volcán Nevado",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Calluha"]
        self.altura = 6025
        self.caracteristicas = [
            "Volcán nevado",
            "Zona de Arequipa",
            "Forma cónica"
        ]


class ApuUarancante(ApuBase):
    """Representa al Apu Uarancante, un pico andino de Puno."""
    def __init__(self):
        super().__init__(
            nombre="Uarancante",
            color=(255, 255, 150),
            health=89,
            bioma="Pico Andino",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Inti"]
        self.altura = 5800
        self.caracteristicas = [
            "Pico andino",
            "Zona de Puno",
            "Nevado"
        ]


class ApuAllincapac(ApuBase):
    """Representa al Apu Allincapac, conocido como la Montaña Dorada."""
    def __init__(self):
        super().__init__(
            nombre="Allincapac",
            color=(255, 215, 0),
            health=93,
            bioma="Montaña Dorada",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Killa"]
        self.altura = 5900
        self.caracteristicas = [
            "Montaña dorada",
            "Zona de Apurímac",
            "Sagrada"
        ]


class ApuKatunqui(ApuBase):
    """Representa al Apu Katunqui, un volcán inactivo de Moquegua."""
    def __init__(self):
        super().__init__(
            nombre="Katunqui",
            color=(200, 100, 255),
            health=85,
            bioma="Volcán Inactivo",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Chaska"]
        self.altura = 5700
        self.caracteristicas = [
            "Volcán inactivo",
            "Zona de Moquegua",
            "Forma redondeada"
        ]


class ApuPatallacta(ApuBase):
    """Representa al Apu Patallacta, asociado a las ruinas sagradas de Cusco."""
    def __init__(self):
        super().__init__(
            nombre="Patallacta",
            color=(139, 69, 19),
            health=100,
            bioma="Ruinas Sagradas",
            gif="coropuna.gif"
        )
        self.illas_robadas = ["Qullqi", "Quispe"]
        self.altura = 2800
        self.caracteristicas = [
            "Ruinas sagradas",
            "Zona de Cusco",
            "Sitio arqueológico"
        ]

# ================== DATOS DEL JUEGO (COMPATIBILIDAD) ==================
APUS_DATA = {
    """Diccionario principal que almacena los datos de cada Apu del juego.

    Cada clave es el nombre del Apu (str), y su valor es un diccionario
    retornado por `get_datos()` que contiene:

    - color: Tupla RGB que representa el color del Apu.
    - health: Entero con la salud inicial del Apu.
    - bioma: Nombre del bioma asociado.
    - gif: Archivo GIF correspondiente al bioma o representación del Apu.

    Este diccionario se utiliza para poblar el árbol binario de Apus.
    """
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

# ================== GIFs de fondo ==================
BIOMA_GIFS = [
    """Lista con las rutas de los GIFs de fondo utilizados para cada bioma.
    
    Cada posición representa una escena diferente del juego:
    1. Huascarán
    2. Misti
    3. Coropuna
    ...
    12. Cotopaxi
    """
    "biomas/primerBio.gif",                 
    "biomas/segundoBio.gif",                
    "biomas/bioma3_glaciar.gif",            
    "biomas/bioma4_altiplano.gif",          
    "biomas/bioma5_desierto_alto.gif",      
    "biomas/bioma6_volcan_activo.gif",      
    "biomas/bioma7_pico_nevado.gif",        
    "biomas/bioma8_cordillera.gif",         
    "biomas/bioma9_laguna_sagrada.gif",     
    "biomas/bioma10_selva_alta.gif",        
    "biomas/bioma11_valle_glaciar.gif",     
    "biomas/bioma12_cima_suprema.gif"       
]

# ================== Música de fondo ==================
BIOMA_MUSIC = [
    """Lista con las rutas de los archivos de música asignados a cada bioma.
    
    La música cambia dinámicamente según el Apu o bioma actual del jugador.
    """
    "music/musica1.mp3",          
    "music/musica_2.mp3",         
    "music/musica3_coropuna.mp3", 
    "music/musica4_ampato.mp3",   
    "music/musica5_chachani.mp3", 
    "music/musica6_sabancaya.mp3",
    "music/musica7_alpamayo.mp3", 
    "music/musica8_yerupaja.mp3", 
    "music/musica9_ausangate.mp3", 
    "music/musica10_salkantay.mp3",
    "music/musica11_chopicalqui.mp3",
    "music/musica12_cotopaxi.mp3"
]

# ================== ILLAS ROBADAS ==================
ILLAS_ROBADAS_POR_ESCENA = [
    """Lista de listas que contiene las illas robadas por cada escena.
    
    Cada sublista representa una escena del juego y contiene los nombres
    de las illas (objetos sagrados) que deben recuperarse en ese nivel.
    """
    ["Tumi", "Chacana"],                 # Escena 1 - Huascarán
    ["Perro Viringo", "Cuy"],            # Escena 2 - Coropuna
    ["Illa", "Torito"],                  # Escena 3 - Misti  
    ["Qullqi", "Quispe"],                # Escena 4 - Ampato
    ["Papa", "Maíz"],                    # Escena 5 - Sara Sara
    ["Huashacara"],                      # Escena 6 - Salkantay
    ["Qori", "Chuño"],                   # Escena 7 - Chachani
    ["Cungalpo"],                        # Escena 8 - Ccarhuarazo
    ["Hizanche"],                        # Escena 9 - Rasuwillka
    ["Calluha"],                         # Escena 10 - Hualca Hualca
    ["Inti"],                            # Escena 11 - Uarancante
    ["Killa"],                           # Escena 12 - Allincapac
    ["Chaska"],                          # Escena 13 - Katunqui
    ["Tumi"]                             # Escena 14 - Patallacta (repetido)
]

# ================== GIFs de illas ==================
ILLAS_GIFS = {
    """Diccionario que asocia el nombre de cada illa con su archivo GIF.

    Este mapeo se utiliza para mostrar visualmente los objetos sagrados
    recolectados por el jugador en las diferentes escenas del juego.
    """
    "Tumi": "illas/tumi.gif",   
    "Chacana": "illas/chacana.gif", 
    "Illa": "illas/illa.gif",
    "Torito": "illas/torito.gif",
    "Perro Viringo": "illas/perro_viringo.gif",
    "Cuy": "illas/cuy.gif",
    "Qullqi": "illas/qullqi.gif",
    "Quispe": "illas/quispe.gif",
    "Qori": "illas/qori.gif",
    "Chuño": "illas/chuno.gif",
    "Papa": "illas/papa.gif",
    "Maíz": "illas/maiz.gif",
    "Calluha": "illas/calluha.gif",
    "Cungalpo": "illas/cungalpo.gif",
    "Hizanche": "illas/hizanche.gif",
    "Huashacara": "illas/huashacara.gif",
    "Inti": "illas/inti.gif",
    "Killa": "illas/killa.gif",
    "Chaska": "illas/chaska.gif"
}


# ================== CARGA DE PREGUNTAS DESDE JSON ==================
import json

def cargar_preguntas_desde_json():
    """
    Carga las preguntas desde un archivo JSON llamado `preguntas.json`.

    Intenta abrir y leer el archivo `preguntas.json`, extrayendo la lista de preguntas 
    bajo la clave "preguntas". Si el archivo no existe o ocurre algún error durante 
    la lectura, carga un conjunto de preguntas por defecto.

    Returns:
        list[dict]: Una lista de diccionarios, donde cada diccionario representa 
        una pregunta con sus opciones y la respuesta correcta.
    """
    try:
        with open("preguntas.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            preguntas = datos["preguntas"]
            print(f"[OK] Cargadas {len(preguntas)} preguntas desde preguntas.json")
            return preguntas
    except FileNotFoundError:
        print("[ERROR] Archivo preguntas.json no encontrado, usando preguntas por defecto")
        return preguntas_por_defecto()
    except Exception as e:
        print(f"[ERROR] Error cargando preguntas.json: {e}, usando preguntas por defecto")
        return preguntas_por_defecto()


def preguntas_por_defecto():
    """
    Devuelve un conjunto de preguntas predefinidas en caso de que falle 
    la carga del archivo JSON.

    Returns:
        list[dict]: Lista de preguntas de respaldo con formato estándar.
    """
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
if __name__ == "__main__":
    PREGUNTAS_APUS = cargar_preguntas_desde_json()



# ================== FUNCIONES ==================
def load_gif_frames(gif_path):
    """
    Carga todos los frames (fotogramas) de un archivo GIF y los convierte 
    en superficies de Pygame.

    Recorre cada frame del GIF utilizando `Pillow (PIL)` y lo transforma 
    en una superficie (`Surface`) compatible con Pygame. Esto permite 
    mostrar animaciones cuadro por cuadro dentro del juego.

    Args:
        gif_path (str): Ruta del archivo GIF a cargar.

    Returns:
        list[pygame.Surface] | None: 
        Lista de superficies Pygame que representan cada frame del GIF, 
        o `None` si ocurre un error durante la carga.
    """
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
    """
    Carga un archivo de música en el mezclador de Pygame.

    Verifica si el archivo existe antes de intentar cargarlo. 
    No reproduce automáticamente la música.

    Args:
        music_path (str): Ruta del archivo de música a cargar.

    Returns:
        bool: `True` si la música fue cargada correctamente, `False` si no se pudo cargar.
    """
    try:
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            return True
        return False
    except Exception as e:
        print(f"Error cargando música {music_path}: {e}")
        return False


def play_music(music_path, loop=-1):
    """
    Reproduce la música de fondo utilizando Pygame.

    Primero intenta cargar el archivo mediante `load_music()`. 
    Si tiene éxito, inicia la reproducción con la cantidad de bucles especificada.

    Args:
        music_path (str): Ruta del archivo de música.
        loop (int, opcional): Número de repeticiones. 
            - `-1`: reproducción infinita (por defecto).
            - `0`: se reproduce una sola vez.

    Returns:
        bool: `True` si la música comenzó a reproducirse correctamente, `False` en caso contrario.
    """
    try:
        if load_music(music_path):
            pygame.mixer.music.play(loop)
            return True
        return False
    except Exception as e:
        print(f"Error reproduciendo música: {e}")
        return False


def stop_music():
    """
    Detiene cualquier música que esté reproduciéndose actualmente.

    No requiere parámetros ni devuelve valores.
    """
    pygame.mixer.music.stop()


def draw_pixelated_hearts(screen, lives, max_lives, x, y):
    """
    Dibuja corazones pixelados (estilo Minecraft) en pantalla para representar vidas.

    Cada corazón se genera con pequeños rectángulos rojos o grises 
    dependiendo de las vidas restantes.

    Args:
        screen (pygame.Surface): Superficie donde se dibujarán los corazones.
        lives (int): Número actual de vidas del jugador.
        max_lives (int): Número máximo de vidas que se pueden mostrar.
        x (int): Coordenada X de inicio del primer corazón.
        y (int): Coordenada Y de inicio del primer corazón.

    Returns:
        None
    """
    heart_size = 20
    spacing = 25
    
    for i in range(max_lives):
        heart_x = x + (i * spacing)
        heart_y = y
        
        if i >= lives:
            color = GRAY
        else:
            color = RED
        
        # Dibujar corazón pixelado con pequeños rectángulos
        pygame.draw.rect(screen, color, (heart_x + 4, heart_y + 2, 4, 4))
        pygame.draw.rect(screen, color, (heart_x + 12, heart_y + 2, 4, 4))
        pygame.draw.rect(screen, color, (heart_x + 2, heart_y + 6, 16, 4))
        pygame.draw.rect(screen, color, (heart_x + 4, heart_y + 10, 12, 4))
        pygame.draw.rect(screen, color, (heart_x + 6, heart_y + 14, 8, 4))
        pygame.draw.rect(screen, color, (heart_x + 8, heart_y + 18, 4, 4))

        
# ================== CLASES DEL JUEGO ==================

class Player:
    """
    Representa al personaje principal Ekeko dentro del juego.

    Controla el movimiento, la animación, la recolección de objetos (illas)
    y la visualización de la mochila.

    Attributes:
        rect (pygame.Rect): Área de colisión y posición del jugador.
        speed (int): Velocidad de movimiento horizontal.
        vel_x (float): Velocidad horizontal actual.
        vel_y (float): Velocidad vertical actual (afectada por la gravedad).
        on_ground (bool): Indica si el jugador está tocando el suelo.
        gravity (float): Fuerza de gravedad aplicada por frame.
        jump_strength (float): Impulso vertical del salto.
        facing_right (bool): Dirección actual del jugador.
        walking (bool): Indica si el jugador se está moviendo horizontalmente.
        frame_index (int): Índice del frame actual de animación.
        animation_speed (float): Velocidad de cambio entre frames.
        animation_timer (float): Temporizador interno para animaciones.
        lives (int): Vidas actuales del jugador.
        max_lives (int): Máximo número de vidas.
        articulos_collected (list[str]): Lista de nombres de illas recolectadas.
        font (pygame.font.Font): Fuente usada para mostrar el nombre “Ekeko”.
        collection_radius (float): Radio de detección para recoger illas cercanas.
        mochila (MochilaVisual): Instancia de la mochila visual.

    Args:
        x (int): Posición inicial en el eje X.
        y (int): Posición inicial en el eje Y.
        gif_path (str, opcional): Ruta del GIF de animación del jugador.
        scale_factor (float, opcional): Factor de escala para redimensionar el sprite.
    """
    def __init__(self, x, y, gif_path=None, scale_factor=1.0):
        ...

    def create_placeholder(self):
        """Crea un sprite temporal (placeholders de colores) si no se encuentra un GIF."""
        ...

    def update(self):
        """Actualiza la posición, la física (gravedad) y la animación del jugador."""
        ...

    def update_animation(self):
        """Cambia los frames del sprite según el movimiento o salto."""
        ...

    def handle_input(self, keys):
        """
        Procesa la entrada del teclado para mover al personaje Ekeko.

        Controles:
            - A: Mover hacia la izquierda.
            - D: Mover hacia la derecha.
            - W: Saltar.
            - J: Mostrar/ocultar mochila (gestionado en GameManager).
            - ↑ / ↓: Navegar entre opciones (en pantallas de preguntas).
            - ENTER: Confirmar respuesta.
        """
        ...

    def lose_life(self):
        """
        Resta una vida al jugador.

        Returns:
            bool: True si aún quedan vidas, False si el jugador muere.
        """
        ...

    def collect_articulos(self, articulos_list):
        """Agrega uno o varios artículos (illas) a la colección del jugador."""
        ...

    def check_collection_proximity(self, articulos_list):
        """
        Verifica si el jugador está lo suficientemente cerca de una illa
        para recolectarla automáticamente.

        Args:
            articulos_list (list[Articulo]): Lista de objetos del tipo Articulo.

        Returns:
            bool: True si se recolectó alguna illa, False en caso contrario.
        """
        ...

    def draw(self, screen):
        """Dibuja al jugador y su nombre en pantalla, junto con la mochila."""
        ...


class Apu:
    """
    Representa a los espíritus guardianes (Apus) que entregan illas al jugador.

    Attributes:
        name (str): Nombre del Apu.
        data (dict): Información del Apu (color, salud, bioma, GIF, etc.).
        health (int): Salud actual del Apu.
        max_health (int): Salud máxima del Apu.
        rect (pygame.Rect): Posición y tamaño del Apu en pantalla.
        frames (list[pygame.Surface]): Frames de animación del GIF del Apu.
        font (pygame.font.Font): Fuente para mostrar el nombre en pantalla.

    Args:
        name (str): Nombre del Apu.
        x (int): Posición X.
        y (int): Posición Y.
        scene_number (int, opcional): Escena actual donde aparece el Apu.
        arbol_apus (ArbolBinario, opcional): Árbol binario con datos de los Apus.
    """
    def __init__(self, name, x, y, scene_number=0, arbol_apus=None):
        ...

    def update(self):
        """Actualiza la animación del Apu."""
        ...

    def draw(self, screen):
        """Dibuja el Apu y su nombre sobre la cabeza."""
        ...

    def give_illas_to_player(self, player, scene_number):
        """
        El Apu entrega las illas robadas al jugador.

        Args:
            player (Player): Instancia del jugador.
            scene_number (int): Número de la escena actual.

        Returns:
            list[str]: Lista de nombres de illas entregadas.
        """
        ...


class Door:
    """
    Representa una puerta que puede abrirse tras completar una escena.

    Attributes:
        rect (pygame.Rect): Rectángulo de colisión y visualización.
        is_open (bool): Estado de la puerta (abierta o cerrada).
        opening_animation (float): Progreso de la animación de apertura.
        font (pygame.font.Font): Fuente para mostrar texto sobre la puerta.
    """
    def __init__(self, x, y):
        ...

    def open_door(self):
        """Abre la puerta (cambia el estado a abierta)."""
        ...

    def update(self):
        """Actualiza el progreso de la animación de apertura."""
        ...

    def draw(self, screen):
        """Dibuja la puerta (cerrada o abriéndose) en pantalla."""
        ...


class Articulo:
    """
    Representa una illa (objeto recolectable) en el mundo del juego.

    Las illas pueden flotar, girar y moverse de forma animada. 
    También pueden tener GIFs asociados.

    Attributes:
        name (str): Nombre de la illa.
        rect (pygame.Rect): Área de colisión y dibujo.
        collected (bool): Indica si la illa fue recolectada.
        frames (list[pygame.Surface] | None): Frames del GIF de la illa.
        rotation_angle (float): Ángulo actual de rotación.
        move_radius (int): Radio del movimiento circular.
        move_speed (float): Velocidad de movimiento circular.
        animation_speed (float): Velocidad de animación del GIF.
    """
    def __init__(self, name, x, y):
        ...

    def update(self):
        """Actualiza las animaciones de flotación, giro y movimiento."""
        ...

    def draw(self, screen):
        """Dibuja la illa (animada o estática) con su nombre debajo."""
        ...


class MochilaVisual:
    """
    Representa la mochila visual donde se muestran las illas recolectadas.

    Permite abrir/cerrar la mochila, mostrar GIFs animados de las illas
    y ver el progreso de colección total.

    Attributes:
        mostrar_mochila (bool): Estado actual de visibilidad.
        illas_guardadas (list[str]): Nombres de las illas recolectadas.
        illas_gifs_cache (dict): Caché de GIFs ya cargados para optimizar rendimiento.
        mochila_gif (bool): Indica si la mochila tiene una animación propia.
    """
    def __init__(self):
        ...

    def agregar_illa(self, illa_name):
        """Agrega una illa al inventario y carga su animación si existe."""
        ...

    def _cargar_gif_illa(self, illa_name):
        """Carga los frames del GIF de una illa y los guarda en la caché."""
        ...

    def alternar_visibilidad(self):
        """Muestra u oculta la mochila (alternando el estado)."""
        ...

    def update(self):
        """Actualiza las animaciones de la mochila y las illas contenidas."""
        ...

    def draw(self, screen):
        """Dibuja el fondo, los GIFs y los nombres de las illas en la pantalla."""
        ...

            
# ================== PARTE 3 - GAME MANAGER Y SISTEMA PRINCIPAL ==================

class QuestionScreen:
    """
    Pantalla que gestiona las preguntas de los Apus durante el juego.

    Permite mostrar una pregunta, navegar por las opciones, confirmar respuestas 
    y mostrar si el jugador acertó o no.

    Attributes:
        pregunta_data (dict): Datos de la pregunta (texto, opciones, respuesta correcta).
        font_title (pygame.font.Font): Fuente para el título o encabezado.
        font_question (pygame.font.Font): Fuente para el texto de la pregunta.
        font_options (pygame.font.Font): Fuente para las opciones de respuesta.
        selected_option (int): Índice de la opción actualmente seleccionada.
        answered (bool): Indica si la pregunta ya fue respondida.
        correct (bool): Indica si la respuesta seleccionada fue correcta.
        show_result (bool): Determina si se está mostrando el resultado.
        result_timer (int): Temporizador que mantiene visible el resultado.
    """
    def __init__(self, pregunta_data):
        ...

    def handle_input(self, event):
        """
        Gestiona los controles del jugador para responder la pregunta.

        Controles:
            - ↑ / ↓ : Mover entre opciones.
            - ENTER : Confirmar respuesta seleccionada.

        Args:
            event (pygame.event.Event): Evento de teclado capturado.
        """
        ...

    def update(self):
        """Actualiza el temporizador de resultado después de responder."""
        ...

    def draw(self, screen):
        """
        Dibuja la interfaz completa de la pregunta en pantalla.

        Incluye el enunciado, las opciones, las instrucciones de control 
        y el resultado si ya se ha respondido.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja la pregunta.
        """
        ...

    def wrap_text(self, text, font, max_width):
        """
        Divide el texto en múltiples líneas si excede un ancho máximo.

        Args:
            text (str): Texto original.
            font (pygame.font.Font): Fuente utilizada.
            max_width (int): Ancho máximo permitido por línea.

        Returns:
            list[str]: Lista de líneas procesadas.
        """
        ...

    def is_finished(self):
        """
        Verifica si el resultado de la pregunta ya ha desaparecido.

        Returns:
            bool: True si el tiempo terminó y se puede continuar.
        """
        ...


class GameScene:
    """
    Representa una escena del juego (un Apu, una puerta y las illas correspondientes).

    Gestiona el comportamiento del Apu, las preguntas, la puerta de salida y 
    la entrega de illas al jugador tras superar la prueba.

    Attributes:
        scene_number (int): Número identificador de la escena.
        apu_name (str): Nombre del Apu correspondiente a esta escena.
        apu (Apu): Instancia del Apu en la escena.
        door (Door): Puerta de salida de la escena.
        question_screen (QuestionScreen | None): Pantalla de pregunta activa.
        completed (bool): Indica si la escena fue superada.
        showing_question (bool): Si se está mostrando la pregunta del Apu.
        player_can_advance (bool): Si el jugador puede pasar a la siguiente escena.
        illas_message (str): Mensaje al recibir illas.
        illas_message_timer (int): Duración del mensaje en pantalla.
        artikulos_visuales (list[Articulo]): Illas visibles y animadas.
    """
    def __init__(self, scene_number, arbol_apus=None):
        ...

    def create_visual_artikulos(self):
        """Crea los artículos visuales (illas) que se mostrarán al superar la escena."""
        ...

    def show_artikulos(self):
        """Muestra visualmente las illas entregadas por el Apu al jugador."""
        ...

    def start_question(self):
        """Inicia la pregunta del Apu al jugador, si no hay otra activa."""
        ...

    def handle_event(self, event, player):
        """
        Procesa los eventos del jugador dentro de la escena, 
        incluyendo la interacción con la pregunta y la recolección de illas.

        Args:
            event (pygame.event.Event): Evento de entrada.
            player (Player): Instancia del jugador.

        Returns:
            str: "CONTINUE" para seguir el juego o "GAME_OVER" si el jugador pierde todas las vidas.
        """
        ...

    def update(self, player):
        """
        Actualiza el estado completo de la escena:
        - Movimiento de illas
        - Estado del Apu y puerta
        - Entrega de objetos
        - Pregunta activa

        Args:
            player (Player): Instancia del jugador.
        """
        ...

    def draw(self, screen, player):
        """
        Dibuja todos los elementos visuales de la escena.

        Incluye:
        - Fondo del bioma
        - Corazones (vidas)
        - Illas recolectadas
        - Apu, puerta y artículos flotantes

        Args:
            screen (pygame.Surface): Superficie donde se dibuja la escena.
            player (Player): Instancia del jugador.
        """
        ...

    def can_advance(self, player):
        """
        Determina si el jugador puede pasar a la siguiente escena.

        Args:
            player (Player): Instancia del jugador.

        Returns:
            bool: True si puede avanzar, False en caso contrario.
        """
        ...


class AnimatedBackground:
    """
    Fondo animado o estático para las escenas del juego.

    Puede usar GIFs animados o colores predefinidos que simulan distintos biomas.

    Attributes:
        scene_number (int): Número de escena para determinar el bioma.
        frames (list[pygame.Surface]): Lista de frames si hay animación GIF.
        background (pygame.Surface): Fondo estático si no hay animación.
        use_gif (bool): Indica si se está usando un GIF o fondo estático.
        animation_speed (float): Velocidad del cambio entre frames.
        animation_timer (float): Temporizador de animación.
    """
    def __init__(self, scene_number=0):
        ...

    def create_biome_background(self):
        """Crea un fondo estático basado en el bioma de la escena."""
        ...

    def update(self):
        """Actualiza el frame actual de la animación si se usa GIF."""
        ...

    def draw(self, screen):
        """
        Dibuja el fondo actual (GIF o color) en la pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibuja el fondo.
        """
        ...



# ================== GAME MANAGER ==================
class GameManager:
    """ Clase principal que controla el flujo general del juego.
    Administra las escenas, el jugador, el árbol de Apus, la música y los diferentes estados del juego.
    """

    def __init__(self):
        """Inicializa todos los componentes esenciales del juego:
        - Crea al jugador, las escenas y el árbol binario de Apus.
        - Configura la música del menú y los estados iniciales.
        """
        self.current_scene = 0
        self.total_scenes = 14  # Actualizado a 14 Apus
        self.scenes = []
        self.player = Player(100, SCREEN_HEIGHT - 250, gif_path="gif.gif", scale_factor=0.1)
        self.background = AnimatedBackground(scene_number=0)
        self.game_state = "MENU"  #  Empieza en el menú principal
        self.font_big = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24, bold=True)

        #  Árbol binario de Apus
        self.arbol_apus = ArbolApus()
        self.poblar_arbol_apus()  # Poblar el árbol con los 14 Apus

        #  Menú principal (definido en archivo separado)
        from menu import MainMenu
        self.main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

        #  Escenas (se crean a partir del árbol binario)
        for i in range(self.total_scenes):
            self.scenes.append(GameScene(i, self.arbol_apus))

        #  Música
        self.current_music = None
        self.load_menu_music()  # Música del menú principal al iniciar


    def poblar_arbol_apus(self):
        """Inserta las clases específicas de los 14 Apus en el árbol binario.
        Además, muestra información de depuración sobre el proceso y estructura final.
        """
        print("Poblando árbol binario con los 14 Apus usando clases específicas...")

        apus_instancias = [
            ApuHuascaran(), ApuCoropuna(), ApuMisti(), ApuAmpato(),
            ApuSaraSara(), ApuSalkantay(), ApuChachani(), ApuCcarhuarazo(),
            ApuRasuwillka(), ApuHualcaHualca(), ApuUarancante(), ApuAllincapac(),
            ApuKatunqui(), ApuPatallacta()
        ]

        for apu in apus_instancias:
            self.arbol_apus.insertar(apu.nombre, apu.get_datos())
            print(f"{apu.nombre} ({apu.bioma}) - Altura: {apu.altura}m - Illas: {apu.illas_robadas}")

        print(f"[OK] Árbol binario poblado con {self.arbol_apus.total_apus} Apus")
        self.arbol_apus.mostrar_arbol()
        self.demostrar_funcionalidades_arbol()


    def demostrar_funcionalidades_arbol(self):
        """Muestra ejemplos prácticos del funcionamiento del árbol binario de Apus:
        - Búsqueda
        - Recorrido inorden
        - Acceso por índice
        - Explicación del orden y jerarquía
        """
        print("\n=== DEMOSTRACIÓN DE FUNCIONALIDADES DEL ÁRBOL BINARIO ===")
        apu_buscado = self.arbol_apus.buscar("Huascarán")
        if apu_buscado:
            print(f"Búsqueda exitosa: {apu_buscado.nombre} - {apu_buscado.datos['bioma']}")
        else:
            print("[ERROR] Apu no encontrado")

        print("\nRecorrido inorden (orden alfabético) de todos los Apus:")
        for i, apu in enumerate(self.arbol_apus.recorrer_inorden()):
            print(f"  {i+1}. {apu.nombre} - {apu.datos['bioma']}")

        print("\nPrimer Apu (orden alfabético):",
              self.arbol_apus.obtener_apu_por_indice(0).nombre)

        print("\nFUNCIONAMIENTO DEL ÁRBOL BINARIO:")
        print("• Los Apus se ordenan alfabéticamente (izquierda < raíz < derecha)")
        print("• Inserción, búsqueda y recorrido basados en comparación de nombres")
        print("=" * 60)


    def load_menu_music(self):
        """Carga y reproduce la música del menú principal."""
        menu_music_path = "music/inicio.mp3"
        if os.path.exists(menu_music_path) and menu_music_path != self.current_music:
            stop_music()
            play_music(menu_music_path)
            self.current_music = menu_music_path
            print("Música del MENÚ principal cargada")


    def load_biome_music(self, scene_number):
        """Cambia la música según el bioma actual."""
        if scene_number < len(BIOMA_MUSIC):
            music_path = BIOMA_MUSIC[scene_number]
            if os.path.exists(music_path) and music_path != self.current_music:
                stop_music()
                play_music(music_path)
                self.current_music = music_path
                print(f"🎵 Música del bioma {scene_number+1}: {music_path}")


    def handle_event(self, event):
        """Gestiona los eventos globales del juego:
        - Navegación entre menús
        - Mostrar instrucciones
        - Jugar, reiniciar o salir
        - Control de la mochila (tecla J)
        """
        if self.game_state == "MENU":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "QUIT"

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
            if not hasattr(self, 'instructions_screen'):
                from menu import InstructionsScreen
                self.instructions_screen = InstructionsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
            if self.instructions_screen.handle_input(event) == "BACK":
                self.game_state = "MENU"

        elif self.game_state == "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                self.player.mochila.alternar_visibilidad()

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
                    if hasattr(self.main_menu, 'menu_music_path'):
                        if os.path.exists(self.main_menu.menu_music_path):
                            play_music(self.main_menu.menu_music_path)

        return "CONTINUE"


    def update(self):
        """Actualiza el estado del juego según el modo actual:
        - Movimiento y animación del jugador
        - Actualización de escenas y fondos
        - Control de progresión entre escenas
        """
        if self.game_state == "MENU":
            self.main_menu.update()

        elif self.game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            self.player.update()
            self.player.mochila.update()
            self.scenes[self.current_scene].update(self.player)

            if self.scenes[self.current_scene].can_advance(self.player):
                self.advance_to_next_scene()

            self.background.update()


    def advance_to_next_scene(self):
        """Pasa a la siguiente escena si el jugador cumple las condiciones."""
        if self.current_scene < self.total_scenes - 1:
            self.current_scene += 1
            self.player.rect.x, self.player.rect.y = 100, SCREEN_HEIGHT - 250
            self.background = AnimatedBackground(scene_number=self.current_scene)
            self.load_biome_music(self.current_scene)
        else:
            self.game_state = "VICTORY"
            stop_music()


    def restart_game(self):
        """Reinicia completamente el juego desde la primera escena."""
        self.current_scene = 0
        self.player = Player(100, SCREEN_HEIGHT - 250, gif_path="gif.gif", scale_factor=0.1)
        self.background = AnimatedBackground(scene_number=0)
        self.game_state = "PLAYING"
        self.scenes = [GameScene(i, self.arbol_apus) for i in range(self.total_scenes)]
        self.load_biome_music(0)


    def draw(self, screen):
        """Dibuja el contenido visual del juego según el estado actual."""
        if self.game_state == "MENU":
            self.main_menu.draw(screen)

        elif self.game_state == "INSTRUCTIONS":
            self.main_menu.draw(screen)
            from menu import InstructionsScreen
            if not hasattr(self, 'instructions_screen'):
                self.instructions_screen = InstructionsScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.instructions_screen.draw(screen)

        elif self.game_state == "PLAYING":
            self.background.draw(screen)
            self.player.draw(screen)
            self.scenes[self.current_scene].draw(screen, self.player)
            self.player.mochila.draw(screen)

            progress_text = self.font_medium.render(f"Progreso: {self.current_scene + 1}/14", True, WHITE)
            screen.blit(progress_text, (SCREEN_WIDTH - 200, 10))

        elif self.game_state == "GAME_OVER":
            self._draw_overlay(screen, "¡GAME OVER!", RED,
                               f"Llegaste hasta la escena {self.current_scene + 1}",
                               f"Illas recuperadas: {len(self.player.articulos_collected)}/19")

        elif self.game_state == "VICTORY":
            self._draw_overlay(screen, "¡VICTORIA TOTAL!", GREEN,
                               "¡Ekeko completó su aventura por los 14 Apus!",
                               f"Illas sagradas recuperadas: {len(self.player.articulos_collected)}/19")


    def _draw_overlay(self, screen, title, color, line1, line2):
        """Dibuja las pantallas finales de 'Game Over' o 'Victory'."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        title_text = self.font_big.render(title, True, color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70))
        screen.blit(title_text, title_rect)

        line1_text = self.font_medium.render(line1, True, WHITE)
        line1_rect = line1_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(line1_text, line1_rect)

        line2_text = self.font_medium.render(line2, True, YELLOW)
        line2_rect = line2_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        screen.blit(line2_text, line2_rect)

        restart_text = self.font_medium.render("Presiona 'R' para reiniciar | 'M' para menú", True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(restart_text, restart_rect)


    def run(self):
        """Bucle principal del juego. Controla eventos, actualización y renderizado."""
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
    """Punto de entrada del programa. Inicia el juego."""
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
