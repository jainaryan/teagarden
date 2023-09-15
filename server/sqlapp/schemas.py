from enum import Enum

from sqlalchemy import DateTime
from pydantic import BaseModel
#from pydantic import Enum
from typing import List, Optional


class EntryType(str, Enum):
    humidity = 'humidity'
    temperature = 'temperature'

class GeoEntityBase(BaseModel):
    name: str
    latitude: Optional[float]
    longitude: Optional[float]
    district: Optional[str]
    state: str
    area: Optional[float]

class GeoEntityCreate(GeoEntityBase):
    pass

class GeoEntity(GeoEntityBase):
    entity_id: int

    class Config:
        orm_mode = True

class StationBase(BaseModel):
    latitude: float
    longitude: float
    sensor_type: str
    sensor_name: str
    garden_id: int

class StationCreate(StationBase):
    pass

class Station(StationBase):
    id: int
    garden: GeoEntity

    class Config:
        orm_mode = True

class RainfallDataBase(BaseModel):
    sensor_id: int
    reading: int
    start_time: str
    end_time: str

class RainfallDataCreate(RainfallDataBase):
    pass

class RainfallData(RainfallDataBase):
    id: int
    station: Station

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
    station: Station

    class Config:
        orm_mode = True




class PurposeType(str, Enum):
    other = 'other'
    research = 'research purpose'
    curious = 'just curious'
    # Add more purposes as needed

class authStatus(str, Enum):
    yes = 'yes'
    no = 'no'

#optional part is getting returned as null need to fix

class UserBase(BaseModel):
    email_id: str
    password: Optional[str] = None
    name: str
    contact_number: int
    authorized: authStatus
  #  purpose: PurposeType

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True