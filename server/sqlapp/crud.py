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
        # Return monthly data
        for year in range(start_year, end_year + 1):
            entities_with_data.extend(get_yearly_or_monthly_data(db, year, is_yearly=False))
    else:
        # Return yearly data
        for year in range(start_year, end_year + 1):
            entities_with_data.extend(get_yearly_or_monthly_data(db, year, is_yearly=True))

    return entities_with_data

def get_yearly_or_monthly_data(db: Session, year: int, is_yearly: bool):
    entities_with_data = []

    # Fetch all GeoEntities
    entities = db.query(GeoEntity).all()

    for entity in entities:
        entity_data = {
            "id": entity.entity_id,
            "name": entity.name,
            "year": year,
            "coordinates": {"longitude": entity.longitude, "latitude": entity.latitude},
            "stations": []
        }

        # Fetch associated stations for the current entity
        stations = db.query(Station).filter_by(entity_id=entity.entity_id).all()

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
                    station_data["data"]["temperature_min"], station_data["data"]["temperature_max"] = temp_humidity_min_max
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

            entity_data["stations"].append(station_data)

        entities_with_data.append(entity_data)

    return entities_with_data
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
