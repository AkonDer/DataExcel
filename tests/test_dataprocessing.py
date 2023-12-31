import os
import sys
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

sys.path.append('./')
from models import Employee, Base
from dataprocessing import DataProcessing

DB_URL = 'sqlite:///:memory:'


@pytest.fixture(scope='function')
def session():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope='function')
def setup_data():
    data = {
        '№': [1, 2, 3, 4, 5],
        'Подразделение': ['АХО', 'Базовая кафедра', 'Сектор разработки', 'Отдел продаж', 'Отдел безопасности'],
        'Сотрудник': ['Иванов Иван Иванович', 'Петров Петр Петрович', 'Сидиков Иван Егорович',
                      'Смолов Владимир Владимирович', 'Егоров Петр Петрович'],
        'Табельный номер': [121, 122, 123, 124, 125],
        'Должность': ['Инженер', 'Научный сотрудник', 'Руководитель проекта', 'Руководитель отдела',
                      'Начальник сектора'],
        'Дата приема': ['01.04.2019', '15.06.2019', '30.09.2019', '10.12.2019', '25.02.2020'],
        'Дата рождения': ['01.04.1990', '15.06.1985', '30.09.1992', '10.12.1978', '25.02.1995'],
        'Адрес по прописке': ['ул. Ленина, 10', 'пр. Победы, 25', 'ул. Советская, 5', 'пер. Гагарина, 8',
                              'пр. Мира, 12']
    }

    df = pd.DataFrame(data)

    yield df.to_excel('test_data.xlsx', index=False)
    os.remove('test_data.xlsx')


def fake_progress_callback(progress):
    # Простая проверка, чтобы удостовериться, что прогресс в допустимом диапазоне
    assert 0 <= progress <= 100


def test_excel_to_db(setup_data, session):
    data_processing = DataProcessing(session)
    data_processing.excel_to_db('test_data.xlsx', fake_progress_callback)
    assert session.query(Employee).count() == 5


def test_clear_db(session):
    # Инициализируем объект DataProcessing
    data_processing = DataProcessing(session)

    # Добавляем запись в базу данных
    employee = Employee(employee_number=126,
                        last_name="Тестов",
                        first_name="Тест",
                        middle_name="Тестович",
                        birth_date=datetime.strptime("01.01.1990", "%d.%m.%Y").date(),
                        address="ул. Тестовая, 1",
                        position="Тестовая должность",
                        department="Тестовый отдел",
                        status="staff member",
                        here_date=datetime.strptime("01.01.2020", "%d.%m.%Y").date())

    session.add(employee)
    session.commit()

    # Убедимся, что запись добавлена
    assert session.query(Employee).count() == 1

    # Вызываем метод clear_db
    data_processing.clear_db()

    # Проверяем, что все записи были удалены из базы данных
    assert session.query(Employee).count() == 0
