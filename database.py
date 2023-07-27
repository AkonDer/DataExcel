# Импорт необходимых библиотек
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee, Base, EmployeeHistory

import unittest

DB_URL = 'sqlite:///employees.db'  # URL для подключения к базе данных SQLite


class EmployeeManager:
    def __init__(self, session):
        self.session = session  # SQLAlchemy session для выполнения операций с базой данных

    def df_to_sql(self, df):
        """
        Записывает данные из pandas DataFrame в таблицу 'employees' в базе данных
        :param df: датафрейм pandas
        :return:
        """
        df.to_sql('employees', self.session.bind, index=False, if_exists='append')

    def create_employee(self, employee_number, last_name, first_name, middle_name, birth_date, address, position,
                        department, status, here_date):
        """
        Создание нового работника и добавление его в базу данных
        :param employee_number: табельный номер
        :param last_name: фамилия
        :param first_name: имя
        :param middle_name: отчество
        :param birth_date: дата рождения
        :param address: адрес
        :param position: должность
        :param department: подразделение (отдел)
        :param status: статус (штатный работник, уволенный, по договору подряда и т.д.
        :param here_date: дата принятия на работу
        :return:
        """
        new_employee = Employee(employee_number=employee_number, last_name=last_name, first_name=first_name,
                                middle_name=middle_name, birth_date=birth_date, address=address, position=position,
                                department=department, status=status, here_date=here_date)
        self.session.add(new_employee)
        self.session.commit()  # Фиксация изменений

    def get_all_employees(self):
        """
        Возвращает все записи из таблицы 'employees' в виде списка объектов класса Employee
        :return: все записи из таблицы 'employees' в виде списка объектов класса Employee
        """
        employees = self.session.query(Employee).all()
        return employees

    def delete_all_employees(self):
        """
        Удаляет все записи из таблицы 'employees'
        :return:
        """
        self.session.query(Employee).delete()
        self.session.query(EmployeeHistory).delete()
        self.session.commit()  # Фиксация изменений

    def close_session(self):
        """
        Закрывает сессию
        :return:
        """
        self.session.close()

    def checking_employee_in_db(self, employee_number) -> bool:
        """
        Проверяет, есть ли такой работников в базе данных по табельному номеру
        :param employee_number: табельный номер работника
        :return: True если такой работника есть в базе данных, иначе False
        """
        result = self.session.query(Employee).filter(Employee.employee_number == employee_number).first()
        if result:
            return True
        return False

    def checking_employee_changes(self, employee_number, last_name, position, department, address, status):
        employee = self.session.query(Employee).filter(Employee.employee_number == employee_number).first()
        old_last_name = None
        old_position = None
        old_department = None
        old_address = None
        old_status = None

        if employee.last_name != last_name or employee.position != position or employee.department != department \
                or employee.address != address or employee.status != status:

            # Проверяем изменения
            if employee.last_name != last_name:
                old_last_name = employee.last_name
                employee.last_name = last_name

            if employee.position != position:
                old_position = employee.position
                employee.position = position

            if employee.department != department:
                old_department = employee.department
                employee.department = department

            if employee.address != address:
                old_address = employee.address
                employee.address = address

            if employee.status != status:
                old_status = employee.status
                employee.status = status

            employee_history = EmployeeHistory(old_last_name=old_last_name, old_position=old_position,
                                               old_department=old_department, old_address=old_address,
                                               old_status=old_status, employee=employee)
            self.session.add(employee_history)
            self.session.commit()


def create_session():
    """
    Создание новой сессии для работы с базой данных
    :return:
    """
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
