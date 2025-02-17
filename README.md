# 📺 Teleprompter Profesional

Un teleprompter profesional desarrollado en Python con PyQt6, diseñado para ofrecer una experiencia de lectura fluida y profesional. Perfecto para presentadores, creadores de contenido y profesionales que necesitan leer guiones con naturalidad.

## ✨ Características

- 📜 **Desplazamiento Suave**: 
  - Control preciso de la velocidad (1-100)
  - Desplazamiento fluido del texto
  - Pausa/Reproducción instantánea
- 🎯 **Línea Guía**: 
  - Línea de referencia central
  - Ayuda a mantener el ritmo de lectura
  - Color personalizable
- 🎙️ **Grabación de Audio**: 
  - Grabación en formato WAV
  - Nombres de archivo con timestamp
  - Almacenamiento automático
- 📊 **Estadísticas en Tiempo Real**: 
  - Palabras por minuto
  - Tiempo transcurrido
  - Progreso de lectura
- 🎨 **Interfaz Profesional**: 
  - Tema oscuro elegante
  - Modo compacto
  - Modo presentación
  - Siempre visible
  - Posición ajustable
- ⚙️ **Personalización**:
  - Tamaño de fuente (12-72pt)
  - Velocidad de desplazamiento
  - Posición de anclaje
  - Opacidad ajustable

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- Tarjeta de sonido (para grabación)
- Windows/Linux/MacOS

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/GuilleO2/promter.git
cd promter
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Unix o MacOS:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

1. Ejecutar el teleprompter:
```bash
python main.py
```

2. Controles Principales:
- 📂 **Cargar Texto**: Botón "Cargar" o arrastra y suelta un archivo
- ▶️ **Iniciar/Detener**: Botón "Iniciar" o Espacio
- 🎚️ **Velocidad**: Deslizador o teclas ← →
- 📝 **Tamaño Texto**: Botones A+ y A-
- 🎙️ **Grabar**: Botón "Grabar"

### ⌨️ Atajos de Teclado

- `Espacio`: Iniciar/Detener desplazamiento
- `F11`: Modo presentación
- `C`: Modo compacto
- `Esc`: Cerrar aplicación
- `←/→`: Ajustar velocidad
- `↑/↓`: Ajustar tamaño de fuente

## 📁 Estructura del Proyecto

```
promter/
├── main.py              # Punto de entrada y lógica principal
├── config.py            # Configuración global
├── ui_components.py     # Componentes de la interfaz
├── audio_recorder.py    # Sistema de grabación
├── stats_manager.py     # Gestión de estadísticas
└── requirements.txt     # Dependencias del proyecto
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz fork del proyecto
2. Crea una nueva rama (`git checkout -b feature/NuevaCaracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añade nueva característica'`)
4. Haz push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📫 Contacto

Guillermo Olmedo - [@GuilleO2](https://github.com/GuilleO2)

Link del proyecto: [https://github.com/GuilleO2/promter](https://github.com/GuilleO2/promter)
