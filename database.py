from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee, Base


DB_URL = 'sqlite:///employees.db'


class EmployeeManager:
    def __init__(self, session):
        self.session = session

    def df_to_sql(self, df):
        df.to_sql('employees', self.session.bind, index=False, if_exists='append')

    def create_employee(self, employee_number, last_name, first_name, middle_name, birth_date, address, position,
                        department, status, here_date):
        new_employee = Employee(employee_number=employee_number, last_name=last_name, first_name=first_name,
                                middle_name=middle_name, birth_date=birth_date, address=address, position=position,
                                department=department, status=status, here_date=here_date)
        self.session.add(new_employee)
        self.session.commit()

    def get_all_employees(self):
        employees = self.session.query(Employee).all()
        return employees

    def delete_all_employees(self):
        self.session.query(Employee).delete()
        self.session.commit()

    def close_session(self):
        self.session.close()


def create_session():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == '__main__':
    session = create_session()
    manager = EmployeeManager(session)

    # manager.generate_fake_employees(10)
    # manager.delete_all_employees()

    employees = manager.get_all_employees()
    # for employee in employees:
    #     print(employee.first_name, employee.position, employee.birth_date, employee.department)

    print(employees)

    manager.close_session()
