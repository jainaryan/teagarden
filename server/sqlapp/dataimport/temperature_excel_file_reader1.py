from datetime import datetime

from numpy import NaN

from common_helper_functions import *


def temperature_type_1_reader(workbook):
    first_sheet = True
    for sheet in workbook._sheets:
        if first_sheet:
            entityName, entity_id, station_id, latitude, longitude, district, state, area, unit = read_values(sheet)
            if check_entity_name(entityName):
                if (entity_id == None):
                    entity_id = get_entity_id(entityName)
                    station_count = count_stations_for_entity(entity_id)
                    if station_count == 1:
                        # Return the station ID
                        station_id = get_station_id_for_entity(entity_id)



            else:
                # entity not in table
                geoEntity_entry(name=entityName, latitude=latitude, longitude=longitude, district=district, state=state,
                                area=area)
                entity_id = get_entity_id(entityName)
                station_id = create_station_entry(entity_id)
            first_sheet = False
        else:
            input_data_from_excel(sheet,station_id,unit)


def input_data_from_excel(sheet, station_id, unit):
    first_month = 2
    last_month = 25
    first_day = 7
    year_row, year_column = find_year(sheet)
    temp_year = sheet.cell(row = year_row, column = year_column).value
    year = get_year(temp_year)
    for month in range(first_month, last_month + 1, 2):
        last_day = find_last_day_of_month(month, int(year)) + 6
        for day in range(29, last_day + 1):
            date = convert_date(year, int(month / 2), day - 6)
            min_reading = get_reading(sheet, unit, day, month+1, year)
            max_reading = get_reading(sheet, unit, day, month, year)

            temperature_entry(station_id, min_reading, max_reading, date)


def temperature_entry(station_id: int, min_reading: float, max_reading: float, date: datetime):
    temperatureData = DailyTemperatureAndHumidityRangeData(station_id=station_id, min_reading=min_reading, max_reading = max_reading, dataType = 'temperature', date = date)
    db_session.add(temperatureData)
    db_session.commit()


def get_reading(sheet, unit, day, month, year):
    if sheet.cell(row = day, column  = month).value == 'N/A':
        return NaN

    reading = float(sheet.cell(row=day, column=month).value)

    if (unit == 'celsius'):
        pass
    elif (unit == 'fahrenheit'):
        reading = float((reading - 32) * 5 / 9)

    reading = round(reading, 2)

    return reading



def check_min_max(month):
    if (month%2==0):
        return 'min'
    else:
        return 'max'


def find_last_day_of_month(month: int, year: int):
    if (month == 4):
        if (year % 4) == 0:
            return 29
        else:
            return 28
    elif (month == 2 or month == 6 or month == 10 or month == 14 or month == 16 or month  == 20 or month == 24):
        return 31
    else :
        return 30


def convert_date(year: int, month: int, day: int):
    temp_date = "" + str(year) + "-" + str(month) + "-" + str(day)
    converted_date = datetime.strptime(temp_date, '%Y-%m-%d').date()
    return converted_date