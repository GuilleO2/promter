import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QTextEdit, QPushButton, QFileDialog, QSlider, QLabel)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

class Prompter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Configuración principal de la ventana
        self.setWindowTitle('Prompter Simple')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |  # Siempre visible
            Qt.WindowType.FramelessWindowHint     # Sin bordes
        )

        # Widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Área de texto
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont('Arial', 20))
        
        # Configurar colores (texto blanco sobre fondo negro)
        palette = self.text_area.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor('black'))
        palette.setColor(QPalette.ColorRole.Text, QColor('white'))
        self.text_area.setPalette(palette)

        # Controles
        self.controls = QWidget()
        controls_layout = QVBoxLayout(self.controls)

        # Botones
        self.load_button = QPushButton('Cargar Texto')
        self.start_button = QPushButton('Iniciar/Pausar')
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_label = QLabel('Velocidad: 50')
        
        # Configurar slider
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.valueChanged.connect(self.update_speed)

        # Añadir widgets al layout de controles
        controls_layout.addWidget(self.load_button)
        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.speed_label)
        controls_layout.addWidget(self.speed_slider)

        # Añadir widgets al layout principal
        layout.addWidget(self.text_area)
        layout.addWidget(self.controls)

        # Timer para el scroll
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.scroll_text)
        self.is_scrolling = False

        # Conectar señales
        self.load_button.clicked.connect(self.load_text)
        self.start_button.clicked.connect(self.toggle_scroll)

        # Mostrar ventana
        self.show()

    def load_text(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir archivo', '', 'Archivos de texto (*.txt)')
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.text_area.setText(file.read())

    def toggle_scroll(self):
        if self.is_scrolling:
            self.scroll_timer.stop()
        else:
            self.scroll_timer.start(50)  # Actualizar cada 50ms
        self.is_scrolling = not self.is_scrolling

    def scroll_text(self):
        scrollbar = self.text_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.value() + 1)
        if scrollbar.value() >= scrollbar.maximum():
            self.scroll_timer.stop()
            self.is_scrolling = False

    def update_speed(self):
        speed = self.speed_slider.value()
        self.speed_label.setText(f'Velocidad: {speed}')
        self.scroll_timer.setInterval(110 - speed)  # Ajustar intervalo según velocidad

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Space:
            self.toggle_scroll()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Prompter()
    sys.exit(app.exec())
