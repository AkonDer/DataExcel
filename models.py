from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    employee_number = Column(Integer)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    birth_date = Column(Date)
    address = Column(String)
    position = Column(String)
    department = Column(String)
    status = Column(String)
    here_date = Column(Date)
    history = relationship("EmployeeHistory", backref='employee')


class EmployeeHistory(Base):
    __tablename__ = 'employees_history'

    history_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.now)
    old_last_name = Column(String)
    old_position = Column(String)
    old_department = Column(String)
    old_address = Column(String)
    old_status = Column(String)
