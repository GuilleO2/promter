"""Componentes de la interfaz de usuario"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                            QPushButton, QSlider, QLabel, QFrame, QSpinBox,
                            QStyle, QProgressBar, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
import config
from datetime import datetime
import os

class GuideLineWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(config.GUIDE_HEIGHT)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {config.GUIDE_COLOR};
                border: none;
                margin: 0px;
            }}
        """)
        # Hacer que la línea guía esté siempre visible
        self.raise_()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

class TitleBar(QWidget):
    minimize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    presentation_mode_toggled = pyqtSignal(bool)
    compact_mode_toggled = pyqtSignal(bool)
    dock_position_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.dock_position = config.DEFAULT_DOCK
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Título
        title = QLabel("Prompter")
        title.setStyleSheet("color: white; font-size: 14px;")
        
        # Botón de modo compacto
        self.compact_btn = QPushButton("⚡")
        self.compact_btn.setFixedSize(20, 20)
        self.compact_btn.setCheckable(True)
        self.compact_btn.clicked.connect(self.compact_mode_toggled.emit)
        self.compact_btn.setToolTip("Modo compacto")
        self.compact_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #333333;
                color: white;
            }
            QPushButton:checked {
                background-color: #333333;
            }
            QPushButton:hover {
                border: 1px solid #444444;
            }
        """)
        
        # Botón de posición (arriba/abajo)
        self.position_btn = QPushButton("↓")
        self.position_btn.setFixedSize(20, 20)
        self.position_btn.clicked.connect(self.toggle_position)
        self.position_btn.setToolTip("Cambiar posición")
        self.position_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #333333;
                color: white;
            }
            QPushButton:hover {
                background-color: #333333;
                border: 1px solid #444444;
            }
        """)
        
        # Botón de modo presentación
        self.presentation_btn = QPushButton("👁")
        self.presentation_btn.setFixedSize(20, 20)
        self.presentation_btn.setCheckable(True)
        self.presentation_btn.clicked.connect(self.presentation_mode_toggled.emit)
        self.presentation_btn.setToolTip("Modo presentación")
        self.presentation_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #333333;
                color: white;
            }
            QPushButton:checked {
                background-color: #333333;
            }
            QPushButton:hover {
                border: 1px solid #444444;
            }
        """)
        
        # Botones de control
        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(20, 20)
        minimize_btn.clicked.connect(self.minimize_clicked.emit)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #333333;
                color: white;
            }
            QPushButton:hover {
                background-color: #333333;
                border: 1px solid #444444;
            }
        """)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.close_clicked.emit)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                border: 1px solid #333333;
                color: white;
            }
            QPushButton:hover {
                background-color: #aa0000;
                border: 1px solid #ff0000;
            }
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.compact_btn)
        layout.addWidget(self.position_btn)
        layout.addWidget(self.presentation_btn)
        layout.addWidget(minimize_btn)
        layout.addWidget(close_btn)
        
        self.setStyleSheet("background-color: #000000;")
        self.setFixedHeight(25)
        
    def toggle_position(self):
        current_index = config.DOCK_POSITIONS.index(self.dock_position)
        next_index = (current_index + 1) % len(config.DOCK_POSITIONS)
        self.dock_position = config.DOCK_POSITIONS[next_index]
        self.position_btn.setText("↑" if self.dock_position == "top" else "↓")
        self.dock_position_changed.emit(self.dock_position)

class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Progreso
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        
        self.progress_label = QLabel("Progreso:")
        self.progress_label.setStyleSheet("color: white;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar, 1)
        
        # Palabras por minuto y tiempo
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.wpm_label = QLabel("0 PPM")
        self.wpm_label.setStyleSheet("color: white;")
        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("color: white;")
        
        stats_layout.addWidget(self.wpm_label)
        stats_layout.addWidget(self.time_label)
        stats_layout.addStretch()
        
        layout.addLayout(progress_layout)
        layout.addLayout(stats_layout)
        
    def update_stats(self, progress, wpm, elapsed_time):
        """Actualiza las estadísticas mostradas"""
        self.progress_bar.setValue(int(progress))
        self.wpm_label.setText(f"{int(wpm)} PPM")
        
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

class RecordingControls(QWidget):
    start_recording = pyqtSignal()
    stop_recording = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Botón de grabación
        self.record_btn = QPushButton("Grabar")
        self.record_btn.setCheckable(True)
        self.record_btn.clicked.connect(self.on_record_clicked)
        
        # Etiqueta de estado
        self.status_label = QLabel("Listo")
        self.status_label.setStyleSheet("color: white;")
        
        layout.addWidget(self.record_btn)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
    def on_record_clicked(self):
        """Maneja el clic en el botón de grabación"""
        if not self.is_recording:
            self.start_recording.emit()
            self.record_btn.setText("Detener")
            self.status_label.setText("Grabando...")
        else:
            self.stop_recording.emit()
            self.record_btn.setText("Grabar")
            self.status_label.setText("Listo")
        self.is_recording = not self.is_recording
        
    def set_recording_state(self, is_recording):
        """Actualiza el estado de grabación y la interfaz"""
        self.is_recording = is_recording
        self.record_btn.setChecked(is_recording)
        self.record_btn.setText("Detener" if is_recording else "Grabar")
        self.status_label.setText("Grabando..." if is_recording else "Listo")

class TimerControls(QWidget):
    timer_started = pyqtSignal()
    timer_stopped = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.remaining_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # Spinner para minutos
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 99)
        self.minutes_spin.setValue(5)
        self.minutes_spin.setStyleSheet("""
            QSpinBox {
                background-color: #444444;
                color: white;
                border: none;
            }
        """)
        
        # Botón de inicio/pausa
        self.start_btn = QPushButton("⏱")
        self.start_btn.setFixedSize(30, 30)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                border: none;
                color: white;
                border-radius: 15px;
            }
            QPushButton:checked {
                background-color: #2a82da;
            }
        """)
        self.start_btn.setCheckable(True)
        self.start_btn.clicked.connect(self.toggle_timer)
        
        # Display del tiempo
        self.time_display = QLabel("00:00")
        self.time_display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)
        
        layout.addWidget(QLabel("Minutos:"))
        layout.addWidget(self.minutes_spin)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.time_display)
        layout.addStretch()
        
    def toggle_timer(self):
        if self.start_btn.isChecked():
            self.remaining_time = self.minutes_spin.value() * 60
            self.timer.start(1000)
            self.timer_started.emit()
        else:
            self.timer.stop()
            self.timer_stopped.emit()
            
    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.time_display.setText(f"{minutes:02d}:{seconds:02d}")
        else:
            self.timer.stop()
            self.start_btn.setChecked(False)
            self.timer_stopped.emit()

class SpeedControls(QWidget):
    speed_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Etiqueta de velocidad
        self.speed_label = QLabel(f"Velocidad: {config.DEFAULT_SPEED}")
        self.speed_label.setStyleSheet("color: white;")
        
        # Slider de velocidad
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(config.MIN_SPEED)
        self.speed_slider.setMaximum(config.MAX_SPEED)
        self.speed_slider.setValue(config.DEFAULT_SPEED)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333333;
                height: 4px;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #cccccc;
            }
        """)
        
        layout.addWidget(self.speed_label)
        layout.addWidget(self.speed_slider)
        
    def on_speed_changed(self, value):
        self.speed_label.setText(f"Velocidad: {value}")
        self.speed_changed.emit(value)

class FontControls(QWidget):
    font_size_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Etiqueta
        self.font_label = QLabel("Tamaño: ")
        self.font_label.setStyleSheet("color: white;")
        
        # Control de tamaño
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(config.MIN_FONT_SIZE, config.MAX_FONT_SIZE)
        self.size_spinbox.setValue(config.DEFAULT_FONT_SIZE)
        self.size_spinbox.valueChanged.connect(self.on_font_size_changed)
        self.size_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #333333;
                color: white;
                border: none;
                padding: 5px;
                min-width: 60px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #444444;
                border: none;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #555555;
            }
        """)
        
        # Botones de ajuste rápido
        decrease_btn = QPushButton("A-")
        decrease_btn.clicked.connect(self.decrease_font)
        increase_btn = QPushButton("A+")
        increase_btn.clicked.connect(self.increase_font)
        
        layout.addWidget(self.font_label)
        layout.addWidget(decrease_btn)
        layout.addWidget(self.size_spinbox)
        layout.addWidget(increase_btn)
        
    def on_font_size_changed(self, size):
        self.font_size_changed.emit(size)
        
    def increase_font(self):
        current = self.size_spinbox.value()
        self.size_spinbox.setValue(min(current + 2, config.MAX_FONT_SIZE))
        
    def decrease_font(self):
        current = self.size_spinbox.value()
        self.size_spinbox.setValue(max(current - 2, config.MIN_FONT_SIZE))

class Controls(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Contenedor principal
        main_container = QWidget()
        main_container.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QProgressBar {
                border: 1px solid #333333;
                border-radius: 2px;
                background-color: #1a1a1a;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
            }
        """)
        
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Botones principales
        buttons_container = QHBoxLayout()
        buttons_container.setSpacing(10)
        
        self.load_button = QPushButton("Cargar Texto")
        self.start_button = QPushButton("Iniciar")
        self.start_button.setCheckable(True)
        
        buttons_container.addWidget(self.load_button)
        buttons_container.addWidget(self.start_button)
        main_layout.addLayout(buttons_container)
        
        # Panel de estadísticas
        self.stats_panel = StatsPanel()
        main_layout.addWidget(self.stats_panel)
        
        # Controles de velocidad
        self.speed_controls = SpeedControls()
        main_layout.addWidget(self.speed_controls)
        
        # Controles de fuente
        self.font_controls = FontControls()
        main_layout.addWidget(self.font_controls)
        
        # Controles de grabación
        self.recording_controls = RecordingControls()
        main_layout.addWidget(self.recording_controls)
        
        # Controles de tiempo
        self.timer_controls = TimerControls()
        main_layout.addWidget(self.timer_controls)
        
        layout.addWidget(main_container)

class TextArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Editor de texto
        self.editor = QTextEdit()
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
                padding: 10px;
            }
        """)
        self.editor.setFont(QFont(config.FONT_FAMILY, config.DEFAULT_FONT_SIZE))
        
        # Contenedor para el editor y la línea guía
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Añadir editor al contenedor
        container_layout.addWidget(self.editor)
        
        # Línea guía
        self.guide_line = GuideLineWidget(container)
        
        # Añadir contenedor al layout principal
        layout.addWidget(container)
        
        # Actualizar posición inicial de la línea guía
        self.update_guide_line_position()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_guide_line_position()
        
    def update_guide_line_position(self):
        # Calcular posición de la línea guía
        guide_y = int(self.height() * config.GUIDE_POSITION)
        self.guide_line.setGeometry(0, guide_y, self.width(), config.GUIDE_HEIGHT)
        # Asegurar que la línea guía esté siempre visible
        self.guide_line.raise_()
        
    def verticalScrollBar(self):
        return self.editor.verticalScrollBar()

    def setText(self, text):
        self.editor.setText(text)
