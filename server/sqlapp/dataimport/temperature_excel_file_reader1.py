from datetime import datetime

from common_helper_functions import *


def temperature_type_1_reader(workbook):
    first_sheet = True
    for sheet in workbook._sheets:
        if first_sheet:
            entityName, entity_id, station_id, latitude, longitude, district, state, area, unit = read_values(sheet)
            if check_entity_name(entityName):
                # entity in table
                pass
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
    temp_year = sheet.cell(row = year_row, column = year_column)
    year = get_year(temp_year)
    for month in range(first_month, last_month + 1):
        last_day = find_last_day_of_month(month, int(year)) + 7
        for day in range(first_day, last_day + 1):
            reading = float(sheet.cell(row=day, column=month).value)
            if (unit == 'Celsius'):
                pass
            elif (unit == 'Farenheit'):
                reading = float((reading - 32) * 5/9)
            reading = round(reading, 2)
            date = convert_date(year, int(month/2), day - 6)
            if (check_min_max(month) == 'min'):

            else:



def temperature_entry(station_id: int, reading: float, day: datetime, ):
    rainfalldata = RainfallData(station_id=station_id, reading=reading, start_time=start_time,
                                end_time=end_time)
    db_session.add(rainfalldata)
    db_session.commit()



def check_min_max(month):
    if (month%2==0):
        return 'min'
    else:
        return 'max'


def find_last_day_of_month(month: int, year: int):
    if (month == 4 or month == 5):
        if (year % 4) == 0:
            return 29
        else:
            return 28

    elif (month == 2 or month == 3 or month == 6 or month == 7 or month == 10 or month  == 11 or month == 14 or month == 15 or month == 16 or month  == 17 or month == 20 or month == 21 or month == 24 or month == 25 ):
        return 31
    else :
        return 30


def convert_date(year: int, month: int, day: int):
    temp_date = "" + str(year) + "-" + str(month) + "-" + str(day)
    converted_date = datetime.strptime(temp_date, '%Y-%m-%d').date()

    return converted_date