from datetime import datetime


def date_ref(date):
    date_obj = datetime.strptime(date, "%d.%m.%Y")
    return date_obj.strftime("%Y-%m-%d")
