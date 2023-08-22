from datetime import datetime
import openpyxl
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlapp.config import entry_id

import time

from sqlapp.models import TemperatureAndHumidityData, RainfallData

workbook = openpyxl.load_workbook("Arun Tea Estate (Sonitpur).xlsx", data_only=True)
SQLALCHEMY_DATABASE_URL = "postgresql://admin:pass@localhost/teaGarden"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
base = declarative_base()
db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)


def checkmonth(month: int, year: int):
    if (month == 3):
        if (year % 4 == 0):
            return 29
        else:
            return 28

    elif (month < 9):
        if (month % 2 == 0):
            return 31
        else:
            return 30

    elif (month > 9):
        if (month % 2 == 0):
            return 30
        else:
            return 31
    else:
        return 31


def add_rainfall_data(entry_id: int, value: float, year: int, month: int, day: int):
    base.metadata.create_all(bind=engine)
    temp_date = "" + str(year) + "-" + str(month) + "-" + str(day)
    converted_date = datetime.strptime(temp_date, '%Y-%m-%d').date()
    db_session.add(
        RainfallData(entry_id=entry_id, reading=value, date=converted_date)
    )
    db_session.commit()
    entry_id = entry_id + 1


def add_temp_humidity_data(entry_id: int, type: str, value: float, hour: int, minute: int):
    base.metadata.create_all(bind=engine)
    time_str = "" + str(hour) + "::" + str(minute) + "::" + "00"
    timestamp = time.strptime(time_str, '%H::%M::%S')

    db_session.add(
        TemperatureAndHumidityData(entry_id=entry_id, dataType=type, reading=value, time=timestamp)
    )
    db_session.commit()
    entry_id = entry_id + 1


for sheet in workbook.worksheets:

    temp_year = sheet.cell(row=4, column=7).value
    year = temp_year[4:]
    year = year.strip()
    first_month = 2
    last_month = 13
    first_day = 6

    for month in range(first_month, last_month + 1):

        last_day = checkmonth(month, int(year)) + 5
        for day in range(first_day, last_day + 1):
            reading = sheet.cell(row=day, column=month).value
            # list1.append(reading)
            # print(reading)
            add_rainfall_data(entry_id, reading, year, month - 1, day - 5)
