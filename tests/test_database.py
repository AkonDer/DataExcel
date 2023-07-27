import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime

sys.path.append('./')
from models import Employee, Base
from database import EmployeeManager, create_session, EmployeeHistory

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
def manager(session):
    return EmployeeManager(session)


@pytest.fixture(scope='function')
def employee(manager):
    birth_date = datetime.strptime('1980-01-01', '%Y-%m-%d').date()
    here_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    manager.create_employee(123456, 'Doe', 'John', 'A.', birth_date, 'Some Address', 'Developer', 'IT', 'Active',
                            here_date)
    return manager


def test_df_to_sql(session, manager):
    df = pd.DataFrame({
        'employee_number': [123456],
        'last_name': ['Doe'],
        'first_name': ['John'],
        'middle_name': ['A.'],
        'birth_date': ['1980-01-01'],
        'address': ['Some Address'],
        'position': ['Developer'],
        'department': ['IT'],
        'status': ['Active'],
        'here_date': ['2020-01-01']
    })
    manager.df_to_sql(df)
    result = session.query(Employee).first()
    assert result.employee_number == 123456
    assert result.first_name == 'John'


def test_create_employee(session, employee):
    result = session.query(Employee).first()
    assert result.employee_number == 123456
    assert result.first_name == 'John'


def test_get_all_employees(session, employee):
    employees = employee.get_all_employees()
    assert len(employees) == 1
    assert employees[0].employee_number == 123456


def test_delete_all_employees(session, employee):
    employee.delete_all_employees()
    result = session.query(Employee).all()
    assert len(result) == 0
    result = session.query(EmployeeHistory).all()
    assert len(result) == 0


def test_checking_employee_in_db(employee):
    result = employee.checking_employee_in_db(123456)
    assert result is True
    result = employee.checking_employee_in_db(1234567)
    assert result is False


def test_checking_employee_changes(session, employee):
    # Убеждаемся, что в истории нет записей
    assert session.query(EmployeeHistory).count() == 0

    employee.checking_employee_changes(123456, "Smith", "Programmer", "Some department", "Some Address new",
                                       "Not active")

    # Проверяем, что в истории появилась новая запись
    history_entry = session.query(EmployeeHistory).first()
    assert history_entry is not None
    assert history_entry.old_last_name == "Doe"
    assert history_entry.old_position == "Developer"
    assert history_entry.old_department == "IT"
    assert history_entry.old_address == "Some Address"
    assert history_entry.old_status == "Active"

    employee.checking_employee_changes(123456, "Smith", "Programmer", "Some department", "Some Address new",
                                       "Not active")

    # Убеждаемся, что в истории не появилось новых записей
    assert session.query(EmployeeHistory).count() == 1


def test_create_session():
    session = create_session()
    assert session is not None
    session.close()
