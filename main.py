import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.uic import loadUi
import dataprocessing as dp


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('mainwindow.ui', self)

        self.pushButton_Load_Excel = self.findChild(QPushButton, 'pushButton_Load_Excel')

        # Привязка обработчика события к кнопке
        self.pushButton_Load_Excel.clicked.connect(self.button_clicked)

    def button_clicked(self):
        # Обработчик события нажатия кнопки
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "/", "All Files (*)")
        dp.excel_to_db(filename)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
