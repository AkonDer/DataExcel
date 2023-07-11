from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee, Base

DB_URL = 'sqlite:///employees.db'


class EmployeeManager:
    def __init__(self):
        self.engine = create_engine(DB_URL)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def df_to_sql(self, df):
        df.to_sql('employees', self.engine, index=False, if_exists='append')

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


if __name__ == '__main__':
    manager = EmployeeManager()

    # manager.generate_fake_employees(10)
    # manager.delete_all_employees()

    employees = manager.get_all_employees()
    # for employee in employees:
    #     print(employee.first_name, employee.position, employee.birth_date, employee.department)

    print(employees)

    manager.close_session()
