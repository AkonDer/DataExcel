import pandas as pd
import numpy as np
from database import EmployeeManager, create_session
from datetime import datetime
import asyncio


# Класс для обработки данных
class DataProcessing:
    def __init__(self, session):
        self.session = session

    # Метод для чтения данных из Excel файла и загрузки их в базу данных
    def excel_to_db(self, filename, progress_callback):
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

        # Обход каждой строки в датафрейме
        for index, row in df.iterrows():
            # Разделение имени на фамилию, имя и отчество
            last_name = row[EMPLOYEE].split(' ')[0].strip()
            first_name = row[EMPLOYEE].split(' ')[1].strip()
            middle_name = row[EMPLOYEE].split(' ')[2].strip() if len(row['Сотрудник'].split(' ')) > 2 else np.nan

            # Попытка преобразовать дату рождения из строки
            try:
                birth_date = datetime.strptime(row[BIRTH_DATE], '%d.%m.%Y').date()
            except Exception as e:
                print(f"Произошла следующая ошибка: {e}")
                birth_date = row[BIRTH_DATE].date()

            # Попытка преобразовать дату принятия на работу из строки
            try:
                here_date = datetime.strptime(row[HERE_DATE], '%d.%m.%Y').date()
            except Exception as e:
                print(f"Произошла следующая ошибка: {e}")
                here_date = row[HERE_DATE].date()

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
