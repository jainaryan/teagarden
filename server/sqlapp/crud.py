import calendar

from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from models import *
import calendar
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

# Assuming you have imported your models correctly
from models import GeoEntity, Station, RainfallData, DailyTemperatureAndHumidityRangeData

def get_all_entities_with_data(db: Session, start_year: int, end_year: int):
    entities_with_data = []

    # Check if the range of years is less than 5
    if end_year - start_year + 1 <= 5:
        is_yearly = False  # Fetch monthly data
    else:
        is_yearly = True  # Fetch yearly data

    # Fetch all GeoEntities
    entities = db.query(GeoEntity).all()

    for entity in entities:
        entity_data = get_entity_yearly_or_monthly_data(db, entity.entity_id, is_yearly, start_year, end_year)
        entities_with_data.append(entity_data)

    return entities_with_data

def get_entity_yearly_or_monthly_data(db: Session, entity_id: int, is_yearly: bool, start_year: int, end_year: int):
    entity_with_data = {
        "id": entity_id,
        "years": [],
        "coordinates": None,  # You can add coordinates here if needed
        "stations": []
    }

    # Fetch entity details (you can add coordinates here if needed)
    entity = db.query(GeoEntity).filter(GeoEntity.entity_id == entity_id).first()
    entity_with_data["coordinates"] = {"longitude": entity.longitude, "latitude": entity.latitude}

    # Fetch associated stations for the current entity
    stations = db.query(Station).filter_by(entity_id=entity_id).all()

    # Iterate through years
    for year in range(start_year, end_year + 1):
        year_data = {
            "year": year,
            "stations": []
        }

        # Fetch data for each station
        for station in stations:
            station_data = {
                "station_id": station.id,
                "station_name": station.sensor_name,
                "data": {}
            }

            # Fetch data based on whether it's yearly or monthly
            if is_yearly:
                # Fetch yearly data for TemperatureAndHumidityData
                temp_humidity_min_max = db.query(func.min(DailyTemperatureAndHumidityRangeData.min_reading),
                                                 func.max(DailyTemperatureAndHumidityRangeData.max_reading)). \
                    filter(DailyTemperatureAndHumidityRangeData.station_id == station.id,
                           extract('year', DailyTemperatureAndHumidityRangeData.date) == year).first()
                if temp_humidity_min_max:
                    station_data["data"]["temperature_min"], station_data["data"][
                        "temperature_max"] = temp_humidity_min_max

                # Fetch yearly data for RainfallData
                rainfall_min_max = db.query(func.min(RainfallData.reading), func.max(RainfallData.reading)). \
                    filter(RainfallData.station_id == station.id,
                           extract('year', RainfallData.start_time) == year).first()
                if rainfall_min_max:
                    station_data["data"]["rainfall_min"], station_data["data"]["rainfall_max"] = rainfall_min_max

            else:
                # Fetch monthly data for TemperatureAndHumidityData
                for month in range(1, 13):
                    temp_humidity_min_max = db.query(func.min(DailyTemperatureAndHumidityRangeData.min_reading),
                                                     func.max(DailyTemperatureAndHumidityRangeData.max_reading)). \
                        filter(DailyTemperatureAndHumidityRangeData.station_id == station.id,
                               extract('year', DailyTemperatureAndHumidityRangeData.date) == year,
                               extract('month', DailyTemperatureAndHumidityRangeData.date) == month).first()
                    if temp_humidity_min_max:
                        station_data["data"][f"month_{month}"] = {
                            "temperature_min": temp_humidity_min_max[0],
                            "temperature_max": temp_humidity_min_max[1]
                        }

                    # Fetch monthly data for RainfallData
                    rainfall_min_max = db.query(func.min(RainfallData.reading), func.max(RainfallData.reading)). \
                        filter(RainfallData.station_id == station.id,
                               extract('year', RainfallData.start_time) == year,
                               extract('month', RainfallData.start_time) == month).first()
                    if rainfall_min_max:
                        station_data["data"][f"month_{month}"]["rainfall_min"], station_data["data"][f"month_{month}"][
                            "rainfall_max"] = rainfall_min_max

            year_data["stations"].append(station_data)

        entity_with_data["years"].append(year_data)

    return entity_with_data


def get_garden(db: Session, g_id: int):
    return db.query(GeoEntity).filter(id == g_id).first()


def get_coordinates(entity: GeoEntity):
    coordinates = (entity.latitude, entity.longitude)
    return (coordinates)


'''
def get_state(db: Session, state_name: str):
    entry_ids = (
        db.query(models.SensorData.entry_id)
        .join(models.SensorReading)
        .join(models.GardenAndSensor)
        .join(models.Garden)
        .filter(models.Garden.state == state_name)
        .all()
    )
    return [entry_id for (entry_id,) in entry_ids]

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''
