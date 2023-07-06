from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee, Base
from faker import Faker

DB_URL = 'sqlite:///employees.db'


class EmployeeManager:
    def __init__(self):
        self.engine = create_engine(DB_URL)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

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

    def generate_fake_employees(self, num_employees):
        fake = Faker()
        for _ in range(num_employees):
            first_name = fake.first_name()
            last_name = fake.last_name()
            position = fake.job()
            birth_date = fake.date_of_birth()
            department = fake.random_element(['IT', 'Sales', 'HR', 'Finance'])
            employee_number = fake.random_number(digits=6)
            middle_name = fake.first_name()
            address = fake.address()
            status = fake.random_element(['Active', 'Inactive'])
            here_date = fake.date_between(start_date='-5y', end_date='today')
            self.create_employee(employee_number, last_name, first_name, middle_name, birth_date, address, position,
                                 department, status, here_date)

    def close_session(self):
        self.session.close()


if __name__ == '__main__':
    manager = EmployeeManager()

    # manager.generate_fake_employees(10)
    manager.delete_all_employees()

    employees = manager.get_all_employees()
    for employee in employees:
        print(employee.first_name, employee.position, employee.birth_date, employee.department)

    manager.close_session()
