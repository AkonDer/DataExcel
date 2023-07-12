import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5 import uic
from dataprocessing import DataProcessing
from database import create_session
from tkinter import messagebox


def button_clicked_load_excel():
    filename, _ = QFileDialog.getOpenFileName(None, "Open File", "/", "All Files (*)")
    if filename != '':
        data_processing = DataProcessing(create_session())
        data_processing.excel_to_db(filename)


def button_clicked_cleardb():
    answer = messagebox.askyesno("Сообщение", "Вы уверены, что хотите очистить базу?")
    if answer:
        data_processing = DataProcessing(create_session())
        data_processing.clear_db()
        messagebox.showinfo("Сообщение", "База полностью очищена")


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main window.ui', self)

        self.pushButton_Load_Excel = self.findChild(QPushButton, 'pushButton_Load_Excel')
        self.pushButton_cleardb = self.findChild(QPushButton, 'pushButton_cleardb')

        # Привязка обработчика события к кнопке
        self.pushButton_Load_Excel.clicked.connect(button_clicked_load_excel)
        self.pushButton_cleardb.clicked.connect(button_clicked_cleardb)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())

# TODO: Добавить асинхронность
# TODO: Добавить полосу прогресса