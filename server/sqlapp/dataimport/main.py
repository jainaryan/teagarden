from datetime import datetime
import openpyxl
from sqlalchemy.sql import text
from sqlapp.models import *
from sqlapp.database import db_session, init_db, engine, conn

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


def convert_date(year: int, month: int, day: int):
    temp_date = "" + str(year) + "-" + str(month) + "-" + str(day)
    converted_date = datetime.strptime(temp_date, '%Y-%m-%d').date()
    return converted_date


def main():
    # initializes the database with tables
    init_db()

    workbook = openpyxl.load_workbook(INPUT_EXCEL, data_only=True)

    for sheet in workbook.worksheets:
        #longitude = sheet.cell(row=2, column=15).value
        #latitude = sheet.cell(row=3, column=15).value
        #district = sheet.cell(row=4,column=15).value
        #state = sheet.cell(row=5,column=15).value
        #area = sheet.cell(row=6, column=15).value
        EntityName = sheet.cell(row=1, column=8).value
        if check_entity_name(EntityName):
            entity_id = get_entity_id(EntityName)
            stationid = (db_session.query(Station).filter_by(entity_id=entity_id).first()).id
        else:
            # case where garden name not present in table
            stationName = None
            # need to figure how to get stationName value
            garden_entry(name=EntityName)
            entityid = get_entity_id(EntityName)
            sensor_entry(entity_id=entityid, name=stationName)
            stationid = (db_session.query(Station).filter_by(entity_id=entityid).first()).id
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
                day = convert_date(year, month - 1, day - 5)
                # rainfallData_entry(reading, day)
                rainfallData_entry(station_id=stationid, reading = reading, date=day)


def garden_entry(name: str, area = None, latitude=None, longitude=None, district=None, state='Assam'):

    entity = GeoEntity(name=name, latitude=latitude, longitude=longitude, district=district, state = state, area=area)
    db_session.add(entity)
    db_session.commit()


def get_entity_id(entityName: str):
    entity = db_session.query(GeoEntity).filter_by(name=entityName).first()
    return entity.id


def get_sensor(stationName: str):
    sensor = db_session.query(Station).filter_by(sensor_name=stationName).first()
    return sensor


def test_sensor_entry():
    init_db()
    sensor = Station(latitude=80, longitude=100, sensor_type='rainfall', sensor_name='First')
    db_session.add(sensor)
    db_session.commit()


def sensor_entry(entity_id: int, name=None, lat=None, long=None, type=None):
    init_db()

    if name == None:
        garden = db_session.query(GeoEntity).filter_by(id=entity_id).first()
        name = str(garden.name) + "_sensor" + str(garden.id)
    db_session.add(Station(sensor_name=name, entity_id=entity_id, sensor_type=type, latitude=lat, longitude=long))
    db_session.commit()


def test_rainfalldata_entry(sensor: Station):
    init_db()
    db_session.add(RainfallData(station_id=sensor.id, reading=100, date="1997-01-01"))
    db_session.commit()

def rainfallData_entry(station_id: int, reading: float, date: datetime):
    rainfalldata = RainfallData(station_id = station_id, reading = reading, date = date)
    db_session.add(rainfalldata)
    db_session.commit()



def check_entity_name(entityName: str):
    entity = (db_session.query(GeoEntity).filter_by(name=entityName).first())

    if entity == None:
        # garden is not present in table
        return False
    else:
        # garden is present in table
        return True


def test_temperatureAndHumidity_entry(station: Station, dataType: EntryType, hour: int, minute: int):
    init_db()
    time_str = "" + str(hour) + "::" + str(minute) + "::" + "00"
    time_str = datetime.strptime(time_str, '%H::%M::%S')
    db_session.add(TemperatureAndHumidityData(station_id=station.id, reading=100, timestamp=time_str, dataType=dataType))
    db_session.commit()


def reset_tables():
    init_db()
    sql = text(
        'TRUNCATE public."geoEntity", public."station", public."users",public."rainfallData", public."temperatureAndHumidityData" RESTART IDENTITY;')

    db_session.commit()


if __name__ == '__main__':

    reset_tables()

    init_db()
    #    test_sensor_entry()
    main()

    #    station = get_sensor('First')
    # test_sensorReading_entry()
    # test_garden_entry()
    # test_gardenAndSensor_entry()
    # test_sensorReading_entry()
    #    test_rainfalldata_entry(station)
    #    test_rainfalldata_entry(station)
    #    test_temperatureAndHumidity_entry(station, 'temperature', 12, 11)
#           garden_entry(name="Arun Tea Estate", district='Sonitpur')
#           gardenid = get_garden_id("Arun Tea Estate")
#           sensor_entry(entity_id=gardenid)
