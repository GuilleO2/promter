"""Aplicación principal del prompter"""
import sys
import os
from datetime import datetime
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QWIDGETSIZE_MAX
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont

import config
from ui_components import TextArea, Controls, TitleBar
from audio_recorder import AudioRecorder
from stats_manager import StatsManager

class Prompter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_pos = None
        self.presentation_mode = False
        self.compact_mode = False
        self.recording = False
        self.dock_position = config.DEFAULT_DOCK
        self.start_time = time.time()
        self.initUI()
        
    def initUI(self):
        # Configuración principal de la ventana
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setGeometry(100, 100, config.DEFAULT_WINDOW_WIDTH, config.DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |  # Siempre visible
            Qt.WindowType.FramelessWindowHint     # Sin bordes
        )
        self.setWindowOpacity(config.WINDOW_OPACITY)

        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Establecer color de fondo negro
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QWidget {
                background-color: #000000;
            }
            QScrollBar:vertical {
                background-color: #000000;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #333333;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #000000;
            }
        """)

        # Barra de título
        self.title_bar = TitleBar()
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.close_clicked.connect(self.close)
        self.title_bar.presentation_mode_toggled.connect(self.toggle_presentation_mode)
        self.title_bar.compact_mode_toggled.connect(self.toggle_compact_mode)
        self.title_bar.dock_position_changed.connect(self.change_dock_position)

        # Área de texto
        self.text_area = TextArea()
        
        # Controles
        self.controls = Controls()

        # Añadir widgets al layout principal
        layout.addWidget(self.title_bar)
        layout.addWidget(self.text_area)
        layout.addWidget(self.controls)

        # Timer para el scroll
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.scroll_text)
        self.is_scrolling = False

        # Inicializar grabador de audio
        self.audio_recorder = AudioRecorder()

        # Inicializar gestor de estadísticas
        self.stats_manager = StatsManager(self.text_area.editor)

        # Timer para actualizar estadísticas
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)

        # Conectar señales
        self.connect_signals()
        
        # Variables para redimensionamiento
        self.resizing = False
        self.resize_edge = None
        self.resize_start_pos = None
        self.resize_start_size = None

        # Mostrar ventana
        self.show()

    def connect_signals(self):
        # Botones principales
        self.controls.load_button.clicked.connect(self.load_text)
        self.controls.start_button.clicked.connect(self.toggle_scroll)
        
        # Conectar controles de velocidad
        self.controls.speed_controls.speed_changed.connect(self.update_scroll_speed)
        
        # Conectar controles de fuente
        self.controls.font_controls.font_size_changed.connect(self.update_font_size)
        
        # Conectar controles de grabación
        self.controls.recording_controls.start_recording.connect(self.start_recording)
        self.controls.recording_controls.stop_recording.connect(self.stop_recording)
        
        # Conectar timer
        self.controls.timer_controls.timer_started.connect(self.start_timer)
        self.controls.timer_controls.timer_stopped.connect(self.stop_timer)

    def toggle_presentation_mode(self, enabled):
        self.presentation_mode = enabled
        self.controls.setVisible(not enabled)
        if enabled:
            self.setWindowState(self.windowState() | Qt.WindowState.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowState.WindowFullScreen)

    def toggle_recording(self):
        if not self.recording:
            self.audio_recorder.start_recording()
            self.recording = True
            self.controls.recording_controls.toggle_recording(True)
        else:
            filename = self.audio_recorder.stop_recording()
            self.recording = False
            self.controls.recording_controls.toggle_recording(False)
            if filename:
                self.controls.recording_controls.status_label.setText(f"Guardado: {os.path.basename(filename)}")

    def toggle_compact_mode(self, enabled):
        self.compact_mode = enabled
        if enabled:
            self.setFixedHeight(config.COMPACT_HEIGHT)
            self.setWindowOpacity(config.COMPACT_OPACITY)
            self.controls.setVisible(False)
            self.change_dock_position(self.dock_position)
        else:
            self.setMinimumSize(config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT)
            self.setFixedHeight(QWIDGETSIZE_MAX)  # Permitir redimensionar
            self.resize(self.width(), config.DEFAULT_WINDOW_HEIGHT)
            self.setWindowOpacity(config.WINDOW_OPACITY)
            self.controls.setVisible(True)
            self.move(self.x(), (QApplication.primaryScreen().size().height() - self.height()) // 2)

    def change_dock_position(self, position):
        self.dock_position = position
        if self.compact_mode:
            screen = QApplication.primaryScreen().size()
            if position == 'top':
                self.move(self.x(), 0)
            else:  # bottom
                self.move(self.x(), screen.height() - self.height())

    def update_stats(self):
        """Actualiza las estadísticas de lectura"""
        if not self.is_scrolling:
            return
            
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Calcular progreso
        scrollbar = self.text_area.editor.verticalScrollBar()
        progress = (scrollbar.value() / scrollbar.maximum()) * 100 if scrollbar.maximum() > 0 else 0
        
        # Calcular palabras por minuto
        text = self.text_area.editor.toPlainText()
        total_words = len(text.split())
        words_read = int(total_words * (progress / 100))
        
        if elapsed_time > 0:
            wpm = (words_read / elapsed_time) * 60
        else:
            wpm = 0
            
        # Actualizar panel de estadísticas
        self.controls.stats_panel.update_stats(
            progress=progress,
            wpm=wpm,
            elapsed_time=elapsed_time
        )

    def on_timer_started(self):
        if not self.is_scrolling:
            self.toggle_scroll()

    def on_timer_stopped(self):
        if self.is_scrolling:
            self.toggle_scroll()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Detectar si estamos en el borde de la ventana
            edge_size = 5
            pos = event.pos()
            x, y = pos.x(), pos.y()
            width, height = self.width(), self.height()
            
            if not self.compact_mode and not self.presentation_mode:
                # Determinar qué borde se está arrastrando
                if x < edge_size:
                    if y < edge_size:
                        self.resize_edge = 'top-left'
                    elif y > height - edge_size:
                        self.resize_edge = 'bottom-left'
                    else:
                        self.resize_edge = 'left'
                elif x > width - edge_size:
                    if y < edge_size:
                        self.resize_edge = 'top-right'
                    elif y > height - edge_size:
                        self.resize_edge = 'bottom-right'
                    else:
                        self.resize_edge = 'right'
                elif y < edge_size:
                    self.resize_edge = 'top'
                elif y > height - edge_size:
                    self.resize_edge = 'bottom'
                else:
                    self.resize_edge = None
                
                if self.resize_edge:
                    self.resizing = True
                    self.resize_start_pos = event.globalPosition().toPoint()
                    self.resize_start_size = self.size()
                    return
            
            # Si no estamos redimensionando, permitir mover la ventana
            if y < self.title_bar.height():
                self.last_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.resizing and self.resize_edge:
            delta = event.globalPosition().toPoint() - self.resize_start_pos
            new_size = self.resize_start_size
            
            if 'right' in self.resize_edge:
                new_width = max(self.resize_start_size.width() + delta.x(), config.MIN_WINDOW_WIDTH)
                new_size.setWidth(new_width)
            elif 'left' in self.resize_edge:
                new_width = max(self.resize_start_size.width() - delta.x(), config.MIN_WINDOW_WIDTH)
                if new_width != self.width():
                    self.move(self.x() + (self.width() - new_width), self.y())
                new_size.setWidth(new_width)
            
            if 'bottom' in self.resize_edge:
                new_height = max(self.resize_start_size.height() + delta.y(), config.MIN_WINDOW_HEIGHT)
                new_size.setHeight(new_height)
            elif 'top' in self.resize_edge:
                new_height = max(self.resize_start_size.height() - delta.y(), config.MIN_WINDOW_HEIGHT)
                if new_height != self.height():
                    self.move(self.x(), self.y() + (self.height() - new_height))
                new_size.setHeight(new_height)
            
            self.resize(new_size)
        elif self.last_pos is not None:
            delta = event.globalPosition().toPoint() - self.last_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.last_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = None
            self.resizing = False
            self.resize_edge = None
            self.resize_start_pos = None
            self.resize_start_size = None

    def load_text(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de texto (*.txt)')
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.text_area.setText(file.read())
                self.text_area.editor.verticalScrollBar().setValue(0)
                self.stats_manager.start_tracking()

    def toggle_scroll(self):
        """Alterna entre iniciar y detener el desplazamiento"""
        if not self.is_scrolling:
            self.start_scroll()
        else:
            self.stop_scroll()
            
    def start_scroll(self):
        """Inicia el desplazamiento del texto"""
        if not hasattr(self, 'scroll_timer'):
            self.scroll_timer = QTimer()
            self.scroll_timer.timeout.connect(self.scroll_text)
            
        self.is_scrolling = True
        self.start_time = time.time()
        self.controls.start_button.setText('Detener')
        self.scroll_timer.start(50)  # Actualizar cada 50ms
            
    def stop_scroll(self):
        """Detiene el desplazamiento del texto"""
        if hasattr(self, 'scroll_timer'):
            self.scroll_timer.stop()
        self.is_scrolling = False
        self.controls.start_button.setText('Iniciar')
        self.controls.start_button.setChecked(False)

    def scroll_text(self):
        """Desplaza el texto según la velocidad configurada"""
        if not self.is_scrolling:
            return
            
        scrollbar = self.text_area.editor.verticalScrollBar()
        if scrollbar.value() >= scrollbar.maximum():
            self.stop_scroll()
            return
            
        current_value = scrollbar.value()
        speed = self.controls.speed_controls.speed_slider.value()
        new_value = current_value + (speed / 10)  # Ajustar la velocidad
            
        scrollbar.setValue(int(new_value))

    def update_scroll_speed(self, speed):
        if self.is_scrolling:
            self.scroll_timer.setInterval(int(1000 / speed))  # Convertir velocidad a intervalo

    def update_font_size(self, size):
        """Actualiza el tamaño de la fuente del texto"""
        self.text_area.editor.setFont(QFont(config.FONT_FAMILY, size))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.presentation_mode:
                self.toggle_presentation_mode(False)
                self.title_bar.presentation_btn.setChecked(False)
            else:
                self.close()
        elif event.key() == Qt.Key.Key_Space:
            self.toggle_scroll()
        elif event.key() == Qt.Key.Key_F11:
            self.toggle_presentation_mode(not self.presentation_mode)
            self.title_bar.presentation_btn.setChecked(self.presentation_mode)

    def closeEvent(self, event):
        if self.recording:
            self.audio_recorder.stop_recording()
        event.accept()

    def start_recording(self):
        """Inicia la grabación de audio"""
        if not self.recording:
            self.recording = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(config.RECORDINGS_DIR, f'recording_{timestamp}.wav')
            self.audio_recorder.start_recording(filename)
            self.controls.recording_controls.set_recording_state(True)
            
    def stop_recording(self):
        """Detiene la grabación de audio"""
        if self.recording:
            filename = self.audio_recorder.stop_recording()
            self.recording = False
            self.controls.recording_controls.set_recording_state(False)
            if filename:
                self.controls.recording_controls.status_label.setText(f"Guardado: {os.path.basename(filename)}")

    def start_timer(self):
        pass

    def stop_timer(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Prompter()
    sys.exit(app.exec())
