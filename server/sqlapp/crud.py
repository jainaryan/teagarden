from sqlalchemy.orm import Session
import models


def get_garden(db: Session, g_id: int):
    return db.query(models.GeoEntity).filter(id == g_id).first()

def add_rainfall_data(db: Session, e_id: int):
    rain_data = models.SensorData()


def get_coordinates(entity: models.GeoEntity):
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