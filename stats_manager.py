"""Módulo para manejar estadísticas de lectura"""
from PyQt6.QtCore import QTimer
import config

class StatsManager:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.start_time = None
        self.word_count = 0
        self.current_position = 0
        self.wpm = 0
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.setInterval(config.WORDS_PER_MINUTE_REFRESH)

    def start_tracking(self):
        """Inicia el seguimiento de estadísticas"""
        self.word_count = len(self.text_widget.toPlainText().split())
        self.current_position = self.text_widget.verticalScrollBar().value()
        self.update_timer.start()

    def stop_tracking(self):
        """Detiene el seguimiento de estadísticas"""
        self.update_timer.stop()

    def update_stats(self):
        """Actualiza las estadísticas de lectura"""
        new_position = self.text_widget.verticalScrollBar().value()
        if new_position == self.current_position:
            return

        # Calcular el progreso aproximado
        total_scroll = self.text_widget.verticalScrollBar().maximum()
        progress = new_position / total_scroll if total_scroll > 0 else 0
        
        # Estimar palabras leídas basado en el progreso
        words_read = int(self.word_count * progress)
        
        # Calcular palabras por minuto
        self.wpm = int(words_read * (60 / (config.WORDS_PER_MINUTE_REFRESH / 1000)))
        self.current_position = new_position

    def get_stats(self):
        """Retorna las estadísticas actuales"""
        return {
            'wpm': self.wpm,
            'total_words': self.word_count,
            'progress': (self.current_position / self.text_widget.verticalScrollBar().maximum() * 100)
            if self.text_widget.verticalScrollBar().maximum() > 0 else 0
        }
