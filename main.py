import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.uic import loadUi
import dataprocessing as dp
from tkinter import messagebox


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('mainwindow.ui', self)

        self.pushButton_Load_Excel = self.findChild(QPushButton, 'pushButton_Load_Excel')
        self.pushButton_cleardb = self.findChild(QPushButton, 'pushButton_cleardb')

        # Привязка обработчика события к кнопке
        self.pushButton_Load_Excel.clicked.connect(self.button_clicked_load_excel)
        self.pushButton_cleardb.clicked.connect(self.button_clicked_cleardb)

    def button_clicked_load_excel(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "/", "All Files (*)")
        if filename != '':
            dp.excel_to_db(filename)

    def button_clicked_cleardb(self):
        answer = messagebox.askyesno("Сообщение", "Вы уверены, что хотите очистить базу?")
        if answer:
            dp.clear_db()
            messagebox.showinfo("Сообщение", "База полностью очищена")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
