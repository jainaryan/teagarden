from datetime import datetime
import openpyxl

from sqlalchemy.sql import text
import time

from sqlapp.models import TemperatureAndHumidityData, RainfallData, Sensor,SensorReading, Garden, GardenAndSensor
from sqlapp.database import db_session, init_db

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


def add_temp_humidity_data(entry_id: int, type: str, value: float, hour: int, minute: int):
    time_str = "" + str(hour) + "::" + str(minute) + "::" + "00"
    timestamp = time.strptime(time_str, '%H::%M::%S')

    db_session.add(
        TemperatureAndHumidityData(entry_id=entry_id, dataType=type, reading=value, time=timestamp)
    )
    db_session.commit()





def convert_date(year: int, month: int, day: int):
    temp_date = "" + str(year) + "-" + str(month) + "-" + str(day)
    converted_date = datetime.strptime(temp_date, '%Y-%m-%d').date()
    return converted_date
def rainfallData_entry(value: float, day: datetime):
    init_db()
    db_session.add(
        RainfallData(reading = value, date = day)
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
                #add_rainfall_data(reading, year, month - 1, day - 5)
                day = convert_date(year, month - 1, day - 5)
                rainfallData_entry(reading, day)
def test_garden_entry():
    init_db()
    garden = Garden(
        garden_name = 'testname',
        latitude = 100,
        longitude = 100,
        city_town = 'test_city',
        state = 'test_state',
        sizeofgarden = 50
    )
    db_session.add(garden)
    db_session.commit()

def garden_entry(name: str, city: str, State: str, lat: float, long: float,  area: int):
    init_db()
    db_session.add(
        Garden(garden_name = name, latitude = lat, longitude = long, district = city, state = State, sizeofgarden = area)
    )
    db_session.commit()


def test_sensor_entry():
    init_db()
    sensor = Sensor(latitude = 80,
        longitude = 100,
        sensor_type = 'rainfall',
        sensor_name = 'First')
    db_session.add(sensor)
    db_session.commit()


def sensor_entry(lat: float, long: float, type: str, name: str ):
    init_db()
    db_session.add(
        Sensor(sensor_name = name, sensor_type = type, latitude = lat, longitude = long)
    )
    db_session.commit()


def test_gardenAndSensor_entry():
    init_db()
    gardenandsensor = GardenAndSensor(
        g_id = 1
    )

    db_session.add(gardenandsensor)
    db_session.commit()


def gardenAndSensor_entry(id: int):
    init_db()
    db_session.add(g_id = id)
    db_session.commit()


def test_sensorReading_entry():
    init_db()
    entry = SensorReading(sensor_id = 1)
    db_session.add(entry)
    db_session.commit()


def sensorReading_entry(id: int):
    init_db()
    db_session.add(sensor_id = id)
    db_session.commit()


def test_rainfalldata_entry():
    init_db()
    db_session.add(
        RainfallData(entry_id = 1, reading=100, date="1997-01-01")
    )
    db_session.commit()




def temperatureAndHumidity_entry(value: float, type: str, Timestamp: time):
    init_db()
    if (type == 'temperature'):
        entry_type = 'temperature'
    elif(type == 'humidity'):
        entry_type = 'humidity'
    #need to figure this case out
    else:
        pass

    db_session.add(
        TemperatureAndHumidityData(reading = value, type = entry_type, timestamp = Timestamp)
    )


def reset_tables():
    init_db()
    sql = text('TRUNCATE public."sensorReading", public."sensor", public."garden",public."rainfallData", public."gardenAndSensor" RESTART IDENTITY;')
    results = db_session.execute(sql)
    db_session.commit()



if __name__ == '__main__':
    #main()
    reset_tables()
    test_sensor_entry()
    test_sensorReading_entry()
    test_garden_entry()
    test_gardenAndSensor_entry()
    test_sensorReading_entry()
    test_rainfalldata_entry()





