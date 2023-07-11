import pandas as pd
import numpy as np
from database import EmployeeManager
from datetime import datetime


def excel_to_db(filename):
    EMPLOYEE_NUMBER = 3
    BIRTH_DATE = 6
    ADDRESS = 7
    POSITION = 4
    DEPORTMENT = 1
    HERE_DATE = 5
    EMPLOYEE = 2
    STATUS = 'staff member'

    df = pd.read_excel(filename)
    manager = EmployeeManager()

    for index, row in df.iterrows():
        last_name = row[EMPLOYEE].split(' ')[0].strip()
        first_name = row[EMPLOYEE].split(' ')[1].strip()
        middle_name = row[EMPLOYEE].split(' ')[2].strip() if len(row['Сотрудник'].split(' ')) > 2 else np.nan

        manager.create_employee(row[EMPLOYEE_NUMBER],
                                last_name,
                                first_name,
                                middle_name,
                                datetime.strptime(row[BIRTH_DATE], '%d.%m.%Y').date(),
                                row[ADDRESS],
                                row[POSITION],
                                row[DEPORTMENT],
                                STATUS,
                                datetime.strptime(row[HERE_DATE], '%d.%m.%Y').date())

        print(index, last_name, first_name, middle_name, row[POSITION])

    manager.close_session()
