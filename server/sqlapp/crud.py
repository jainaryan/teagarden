import calendar

from sqlalchemy import func
from sqlalchemy.orm import Session
from models import *


def get_all_entities_with_data(db: Session, year: int):
    entities_with_data = []

    # Fetch all GeoEntities
    entities = db.query(GeoEntity).all()

    for entity in entities:
        entity_data = {
            "id": entity.id,
            "name": entity.name,
            "coordinates": {"longitude": entity.longitude,"latitude": entity.latitude},
            "stations": []  # Add stations data here
        }

        # Fetch associated stations for the current entity
        stations = db.query(Station).filter_by(entity_id=entity.id).all()

        for station in stations:
            station_data = {
                "station_id": station.id,
                "station_name": station.sensor_name,
                "monthly_data": []
            }

            for month in range(1, 13):
                monthly_data = {
                    "month": calendar.month_name[month],
                    "rainfall_min": None,
                    "rainfall_max": None,
                    "temperature_min": None,
                    "temperature_max": None,
                    "humidity_min": None,
                    "humidity_max": None
                }

                # Fetch monthly data for RainfallData
                rainfall_min_max = db.query(func.min(RainfallData.reading), func.max(RainfallData.reading)). \
                    filter(RainfallData.station_id == station.id, func.extract('year', RainfallData.date) == year,
                           func.extract('month', RainfallData.date) == month).first()
                if rainfall_min_max:
                    monthly_data["rainfall_min"], monthly_data["rainfall_max"] = rainfall_min_max

                # Fetch monthly data for TemperatureAndHumidityData
                temp_humidity_min_max = db.query(func.min(TemperatureAndHumidityData.reading),
                                                 func.max(TemperatureAndHumidityData.reading)). \
                    filter(TemperatureAndHumidityData.station_id == station.id,
                           func.extract('year', TemperatureAndHumidityData.timestamp) == year,
                           func.extract('month', TemperatureAndHumidityData.timestamp) == month).first()
                if temp_humidity_min_max:
                    monthly_data["temperature_min"], monthly_data["temperature_max"] = temp_humidity_min_max

                # Similar logic for humidity data

                station_data["monthly_data"].append(monthly_data)

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
