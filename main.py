import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDesktopWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем заголовок окна
        self.setWindowTitle('Пример QMainWindow')
        # Установка размеров окна
        self.resize(800, 500)

        # Получение геометрии доступной области на экране
        available_geometry = QDesktopWidget().availableGeometry()

        # Вычисление координат для центрирования окна
        x = (available_geometry.width() - self.width()) // 2
        y = (available_geometry.height() - self.height()) // 2

        # Расположение окна по центру экрана
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
