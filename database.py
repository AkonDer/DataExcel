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

    def create_employee(self, first_name, last_name, position, birth_date, department):
        new_employee = Employee(first_name=first_name, last_name=last_name, position=position,
                                birth_date=birth_date, department=department)
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
            self.create_employee(first_name, last_name, position, birth_date, department)

    def close_session(self):
        self.session.close()


if __name__ == '__main__':
    manager = EmployeeManager()

    manager.generate_fake_employees(10)
    # manager.delete_all_employees()
    employees = manager.get_all_employees()
    for employee in employees:
        print(employee.first_name, employee.position, employee.birth_date, employee.department)

    manager.close_session()
