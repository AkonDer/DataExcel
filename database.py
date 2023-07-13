# Импорт необходимых библиотек
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee, Base

DB_URL = 'sqlite:///employees.db'  # URL для подключения к базе данных SQLite


class EmployeeManager:
    def __init__(self, session):
        self.session = session  # SQLAlchemy session для выполнения операций с базой данных

    def df_to_sql(self, df):
        # Записывает данные из pandas DataFrame в таблицу 'employees' в базе данных
        df.to_sql('employees', self.session.bind, index=False, if_exists='append')

    def create_employee(self, employee_number, last_name, first_name, middle_name, birth_date, address, position,
                        department, status, here_date):
        # Создание нового работника и добавление его в базу данных
        new_employee = Employee(employee_number=employee_number, last_name=last_name, first_name=first_name,
                                middle_name=middle_name, birth_date=birth_date, address=address, position=position,
                                department=department, status=status, here_date=here_date)
        self.session.add(new_employee)
        self.session.commit()  # Фиксация изменений

    def get_all_employees(self):
        # Возвращает все записи из таблицы 'employees' в виде списка объектов класса Employee
        employees = self.session.query(Employee).all()
        return employees

    def delete_all_employees(self):
        # Удаляет все записи из таблицы 'employees'
        self.session.query(Employee).delete()
        self.session.commit()  # Фиксация изменений

    def close_session(self):
        # Закрывает сессию
        self.session.close()


def create_session():
    # Создание новой сессии для работы с базой данных
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
