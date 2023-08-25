from enum import Enum
from pydantic import BaseModel
#from pydantic import Enum
from typing import List

class EntryType(str, Enum):
    humidity = 'humidity'
    temperature = 'temperature'

class GardenBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    district: str
    state: str
    area: float

class GardenCreate(GardenBase):
    pass

class Garden(GardenBase):
    id: int

    class Config:
        orm_mode = True

class SensorBase(BaseModel):
    latitude: float
    longitude: float
    sensor_type: str
    sensor_name: str
    garden_id: int

class SensorCreate(SensorBase):
    pass

class Sensor(SensorBase):
    id: int
    garden: Garden

    class Config:
        orm_mode = True

class RainfallDataBase(BaseModel):
    sensor_id: int
    reading: int
    date: str

class RainfallDataCreate(RainfallDataBase):
    pass

class RainfallData(RainfallDataBase):
    id: int
    sensor: Sensor

    class Config:
        orm_mode = True

class TemperatureAndHumidityDataBase(BaseModel):
    sensor_id: int
    dataType: EntryType
    reading: float
    timestamp: str

class TemperatureAndHumidityDataCreate(TemperatureAndHumidityDataBase):
    pass

class TemperatureAndHumidityData(TemperatureAndHumidityDataBase):
    id: int
    sensor: Sensor

    class Config:
        orm_mode = True
