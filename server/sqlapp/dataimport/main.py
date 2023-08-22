from datetime import datetime
import openpyxl

import time

from sqlapp.models import TemperatureAndHumidityData, RainfallData, Sensor
from  sqlapp.database import db_session, init_db

INPUT_EXCEL = "Arun Tea Estate (Sonitpur).xlsx"



def checkmonth(month: int, year: int):
    if month == 3:
        if year % 4 == 0:
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
    temp_date = "" + str(year) + "-" + str(month) + "-" + str(day)
    converted_date = datetime.strptime(temp_date, '%Y-%m-%d').date()
    db_session.add(
        RainfallData(entry_id=entry_id, reading=value, date=converted_date)
    )
    db_session.commit()


def add_temp_humidity_data(entry_id: int, type: str, value: float, hour: int, minute: int):
    time_str = "" + str(hour) + "::" + str(minute) + "::" + "00"
    timestamp = time.strptime(time_str, '%H::%M::%S')

    db_session.add(
        TemperatureAndHumidityData(entry_id=entry_id, dataType=type, reading=value, time=timestamp)
    )
    db_session.commit()


def main():
    #initializes the database with tables
    init_db()

    workbook = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)

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
                # ryj to be handled later on
                entry_id = 0
                add_rainfall_data(entry_id, reading, year, month - 1, day - 5)


def test_sensor_entry():
    init_db()
    sensor = Sensor(latitude = 80,
        longitude = 100,
        sensor_type = 'rainfall',
        sensor_name = 'First')
    db_session.add(sensor)
    db_session.commit()


if __name__ == '__main__':
    #main()
    test_sensor_entry()