import pandas as pd
import numpy as np
from database import EmployeeManager, create_session
from datetime import datetime
import asyncio


# Класс для обработки данных
class DataProcessing:
    def __init__(self, session):
        self.session = session

    def _parse_date(self, date_str):
        """
        Вспомогательный метод для преобразования строки даты в объект date.
        """
        try:
            # Пытаемся преобразовать строку в дату
            return datetime.strptime(date_str, '%d.%m.%Y').date()
        except Exception as e:
            # В случае ошибки выводим сообщение и пытаемся вернуть дату из объекта, если это возможно
            print(f"Произошла следующая ошибка: {e}")
            return date_str.date() if hasattr(date_str, 'date') else None

    def excel_to_db(self, filename, progress_callback):
        """
        Метод для чтения данных из Excel файла и загрузки их в базу данных
        :param filename: Имя файла Excel
        :param progress_callback: callback для обновления прогрессбара
        :return:
        """
        # Константы для обращения к колонкам в датафрейме pandas
        EMPLOYEE_NUMBER = 3
        BIRTH_DATE = 6
        ADDRESS = 7
        POSITION = 4
        DEPORTMENT = 1
        HERE_DATE = 5
        EMPLOYEE = 2
        STATUS = 'staff member'

        # Чтение файла Excel
        df = pd.read_excel(filename)
        # Создание менеджера базы данных
        manager = EmployeeManager(self.session)

        # Получение количества строк в датафрейме
        count_rows = df.shape[0]

        # сверка базы данных с информацией их файла excel, если в файле сотрудник отсутствует его статус в базе данных
        # меняется на "уволен"
        employees = manager.get_employees_with('status', 'staff member')
        for employee in employees:
            result = df[df['Табельный номер'] == employee.employee_number]
            if result.empty:
                manager.change_employee_status(employee.employee_number, "dismissed")

        # Обход каждой строки в датафрейме
        for index, row in df.iterrows():

            # Разделение имени на фамилию, имя и отчество
            last_name = row[EMPLOYEE].split(' ')[0].strip()
            first_name = row[EMPLOYEE].split(' ')[1].strip()
            middle_name = row[EMPLOYEE].split(' ')[2].strip() if len(row['Сотрудник'].split(' ')) > 2 else None

            # Проверка на существование сотрудника в базе данных если сотрудник в бд имеется то пропускаем шаг
            if manager.checking_employee_in_db(row[EMPLOYEE_NUMBER]):
                manager.checking_employee_changes(row[EMPLOYEE_NUMBER], last_name, row[POSITION], row[DEPORTMENT],
                                                  row[ADDRESS], STATUS)
                progress = 100 if index == count_rows - 1 else int(index / count_rows * 100)
                progress_callback(progress)
                continue

            # Преобразование строковых представлений дат в объекты date
            birth_date = self._parse_date(row['Дата рождения'])
            here_date = self._parse_date(row['Дата приема'])

            # Создание нового сотрудника в базе данных
            manager.create_employee(row[EMPLOYEE_NUMBER],
                                    last_name,
                                    first_name,
                                    middle_name,
                                    birth_date,
                                    row[ADDRESS],
                                    row[POSITION],
                                    row[DEPORTMENT],
                                    STATUS,
                                    here_date)

            print(index, last_name, first_name, middle_name, row[POSITION])
            # Вычисление и отправка прогресса
            progress = 100 if index == count_rows - 1 else int(index / count_rows * 100)
            progress_callback(progress)

        # Закрытие сессии базы данных
        manager.close_session()

    # Метод для очистки базы данных
    def clear_db(self):
        manager = EmployeeManager(self.session)
        manager.delete_all_employees()
        manager.close_session()
