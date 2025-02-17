"""Configuraciones del prompter"""
import os

# Directorio base de la aplicación
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RECORDINGS_DIR = os.path.join(APP_DIR, 'grabaciones')
RECORDINGS_DIR = os.path.join(APP_DIR, 'recordings')

# Asegurar que el directorio de grabaciones existe
if not os.path.exists(DEFAULT_RECORDINGS_DIR):
    os.makedirs(DEFAULT_RECORDINGS_DIR)

# Configuración de la ventana
WINDOW_TITLE = 'Prompter Simple'
DEFAULT_WINDOW_WIDTH = 600
DEFAULT_WINDOW_HEIGHT = 400
MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 200
WINDOW_OPACITY = 1  # 80% opaco
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Configuración del modo compacto
COMPACT_HEIGHT = 100  # altura en modo compacto
COMPACT_OPACITY = 0.9  # más opaco en modo compacto
DOCK_POSITIONS = ['top', 'bottom']  # posiciones permitidas para el dock
DEFAULT_DOCK = 'bottom'  # posición predeterminada

# Configuración del texto
FONT_FAMILY = 'Arial'
MIN_FONT_SIZE = 12
MAX_FONT_SIZE = 72
DEFAULT_FONT_SIZE = 20
TEXT_COLOR = '#FFFFFF'  # Blanco
BACKGROUND_COLOR = '#000000'  # Negro

# Configuración del scroll
MIN_SPEED = 1  # Velocidad mínima más baja
MAX_SPEED = 100
DEFAULT_SPEED = 25
SCROLL_UPDATE_INTERVAL = 50  # milisegundos

# Configuración de la línea guía
GUIDE_HEIGHT = 2  # altura en píxeles
GUIDE_COLOR = '#FF0000'  # Rojo
GUIDE_POSITION = 0.3  # 30% desde arriba de la ventana

# Configuración de grabación
AUDIO_CHUNK = 1024
AUDIO_FORMAT = 'paInt16'
AUDIO_CHANNELS = 1
AUDIO_RATE = 44100

# Configuración de estadísticas
WORDS_PER_MINUTE_REFRESH = 1000  # ms
DEFAULT_WORDS_PER_MINUTE = 150  # velocidad promedio de lectura

# Configuración de temporizador
TIMER_UPDATE_INTERVAL = 100  # ms
COUNTDOWN_FORMAT = '%M:%S'  # formato de tiempo
