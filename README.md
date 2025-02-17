# Teleprompter Profesional

Un teleprompter profesional desarrollado en Python con PyQt6, diseñado para ofrecer una experiencia de lectura fluida y profesional.

## Características

- **Desplazamiento Suave**: Control preciso de la velocidad de desplazamiento (1-100)
- **Línea Guía**: Línea de referencia para mantener el foco durante la lectura
- **Grabación de Audio**: Capacidad de grabar audio mientras se lee
- **Estadísticas en Tiempo Real**: Monitoreo de palabras por minuto y progreso
- **Interfaz Profesional**: 
  - Tema oscuro
  - Modo compacto
  - Modo presentación
  - Siempre visible
  - Posición ajustable
- **Personalización**:
  - Tamaño de fuente ajustable (12-72pt)
  - Control de velocidad
  - Posición de anclaje (superior/inferior)

## Requisitos

- Python 3.8+
- PyQt6
- PyAudio
- wave

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/TU_USUARIO/teleprompter.git
cd teleprompter
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

## Uso

1. Ejecutar el teleprompter:
```bash
python main.py
```

2. Funciones principales:
- **Cargar Texto**: Botón "Cargar Texto"
- **Iniciar/Detener**: Botón "Iniciar"
- **Ajustar Velocidad**: Control deslizante
- **Ajustar Fuente**: Botones A+ y A-
- **Grabar Audio**: Botón "Grabar"

3. Atajos de teclado:
- `Esc`: Cerrar aplicación
- `F11`: Modo presentación
- `C`: Modo compacto
- `Space`: Iniciar/Detener desplazamiento

## Estructura del Proyecto

```
teleprompter/
├── main.py              # Punto de entrada principal
├── config.py            # Configuración global
├── ui_components.py     # Componentes de la interfaz
├── audio_recorder.py    # Manejo de grabación
├── stats_manager.py     # Gestión de estadísticas
└── requirements.txt     # Dependencias
```

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Contacto

Tu Nombre - [@tu_twitter](https://twitter.com/tu_twitter) - email@example.com

Link del proyecto: [https://github.com/TU_USUARIO/teleprompter](https://github.com/TU_USUARIO/teleprompter)
