from datetime import datetime

from pydantic import BaseModel
from enum import Enum

class GardenBase(BaseModel):
    garden_name: str
    latitude: float
    longitude: float
    city_town: str
    state: str
    sizeofgarden: float

class GardenCreate(GardenBase):
    pass

class Garden(GardenBase):
    g_id: int

    class Config:
        orm_mode = True

class SensorBase(BaseModel):

    latitude: float
    longitude: float
    sensor_type: str
    sensor_name: str
    pass

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    sensor_id: int

    class Config:
        orm_mode = True

class SensorReadingBase(BaseModel):

    pass

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReading(SensorReadingBase):
    entry_id: int
    sensor_id: int
    class Config:
        orm_mode = True

class TimeframeType(str, Enum):
    immediate_measurement = "immediate measurement"
    range_measurement = "range measurement"

class SensorDataBase(BaseModel):
    type: str
    reading: str
    unit: str
    timeframe: TimeframeType
    time: datetime | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

class SensorDataCreate(SensorDataBase):
    pass

class SensorData(SensorDataBase):
    entry_id: int

    class Config:
        orm_mode = True

class GardenAndSensorBase(BaseModel):

    pass

class GardenAndSensorCreate(GardenAndSensorBase):
    pass

class GardenAndSensor(GardenAndSensorBase):
    sensor_id: int
    g_id: int

    class Config:
        orm_mode = True
