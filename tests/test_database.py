import sys
sys.path.append('./')
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee, Base
import pandas as pd
from datetime import datetime

from database import EmployeeManager, create_session  # Предположим, что ваш модуль называется employee_manager

DB_URL = 'sqlite:///:memory:'

@pytest.fixture(scope='function')
def session():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_df_to_sql(session):
    manager = EmployeeManager(session)
    df = pd.DataFrame({'employee_number': [123456], 'last_name': ['Doe'], 'first_name': ['John'], 'middle_name': ['A.'],
                       'birth_date': ['1980-01-01'], 'address': ['Some Address'], 'position': ['Developer'],
                       'department': ['IT'], 'status': ['Active'], 'here_date': ['2020-01-01']})
    manager.df_to_sql(df)
    result = session.query(Employee).first()
    assert result.employee_number == 123456
    assert result.first_name == 'John'


def test_create_employee(session):
    manager = EmployeeManager(session)
    birth_date = datetime.strptime('1980-01-01', '%Y-%m-%d').date()
    here_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    manager.create_employee(123456, 'Doe', 'John', 'A.', birth_date, 'Some Address', 'Developer', 'IT', 'Active', here_date)
    result = session.query(Employee).first()
    assert result.employee_number == 123456
    assert result.first_name == 'John'


def test_get_all_employees(session):
    manager = EmployeeManager(session)
    birth_date = datetime.strptime('1980-01-01', '%Y-%m-%d').date()
    here_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    manager.create_employee(123456, 'Doe', 'John', 'A.', birth_date, 'Some Address', 'Developer', 'IT', 'Active', here_date)
    employees = manager.get_all_employees()
    assert len(employees) == 1
    assert employees[0].employee_number == 123456


def test_delete_all_employees(session):
    manager = EmployeeManager(session)
    birth_date = datetime.strptime('1980-01-01', '%Y-%m-%d').date()
    here_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    manager.create_employee(123456, 'Doe', 'John', 'A.', birth_date, 'Some Address', 'Developer', 'IT', 'Active', here_date)
    manager.delete_all_employees()
    result = session.query(Employee).all()
    assert len(result) == 0


def test_create_session():
    session = create_session()
    assert session is not None
    session.close()
