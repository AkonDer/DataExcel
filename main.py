# Импорт необходимых библиотек
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QProgressBar
from PyQt6 import uic
from dataprocessing import DataProcessing
from database import create_session
from tkinter import messagebox
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool, pyqtSignal, QObject


# Объект для отправки сигналов из Worker'a
class WorkerSignals(QObject):
    # Сигнал для отправки изменений прогресса
    progressChanged = pyqtSignal(int)


# Подкласс QRunnable для выполнения задачи в отдельном потоке
class Worker(QRunnable):
    def __init__(self, filename, data_processing):
        super().__init__()
        self.filename = filename
        self.data_processing = data_processing
        self.signals = WorkerSignals()

    # метод run() будет выполнен в отдельном потоке при вызове start() на объекте QThreadPool
    @pyqtSlot()
    def run(self):
        self.data_processing.excel_to_db(self.filename, self.report_progress)

    # Отправка сигнала об изменении прогресса
    def report_progress(self, progress):
        self.signals.progressChanged.emit(progress)


# Главное окно приложения
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main window.ui', self)

        # Получение ссылок на элементы интерфейса
        self.pushButton_Load_Excel = self.findChild(QPushButton, 'pushButton_Load_Excel')
        self.pushButton_cleardb = self.findChild(QPushButton, 'pushButton_cleardb')
        self.progressBar = self.findChild(QProgressBar, 'progressBar')

        # Привязка обработчиков к кнопкам
        self.pushButton_Load_Excel.clicked.connect(self.button_clicked_load_excel)
        self.pushButton_cleardb.clicked.connect(self.button_clicked_cleardb)

    # Обработчик кнопки загрузки файла
    def button_clicked_load_excel(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", "/", "All Files (*)")
        if filename != '':
            data_processing = DataProcessing(create_session())
            worker = Worker(filename, data_processing)
            # Подключаем сигнал progressChanged к setValue слоту progressBar, что позволит обновлять его значение
            worker.signals.progressChanged.connect(self.progressBar.setValue)
            # Начинаем выполнение задачи в отдельном потоке
            QThreadPool.globalInstance().start(worker)

    # Обработчик кнопки очистки базы данных
    def button_clicked_cleardb(self):
        answer = messagebox.askyesno("Сообщение", "Вы уверены, что хотите очистить базу?")
        if answer:
            data_processing = DataProcessing(create_session())
            data_processing.clear_db()
            messagebox.showinfo("Сообщение", "База полностью очищена")


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
