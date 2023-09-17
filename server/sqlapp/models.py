




import enum
from sqlalchemy import DATETIME, DateTime

import timestamp as timestamp
from passlib.hash import bcrypt
from sqlapp.database import base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Date, Time, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Enum


class GeoEntity(base):
    __tablename__ = 'geoEntity'

    entity_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    district = Column(String(20), nullable=True)
    state = Column(String(20), nullable=False)
    area = Column(Float, nullable=True)


class Station(base):
    __tablename__ = 'station'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sensor_type = Column(String(50), nullable=True)
    sensor_name = Column(String(50), nullable=True, unique=True)
    entity_id = Column(Integer, ForeignKey('geoEntity.entity_id'), nullable=False)

    geoEntity = relationship('GeoEntity')




class RainfallData(base):
    __tablename__ = 'rainfallData'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('station.id'))
    reading = Column(Float)
    #date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    station = relationship('Station')


class EntryType(enum.Enum):
    humidity = 'humidity'
    temperature = 'temperature'


class TemperatureAndHumidityInstantaneousData(base):

    __tablename__ = 'temperatureAndHumidityInstantaneousData'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('station.id'))
    dataType = Column(Enum(EntryType))
    reading = Column(Float)
    timestamp = Column(Time)
    # Establish a relationship with Sensor
    station = relationship('Station')

class DailyTemperatureAndHumidityRangeData(base):
    __tablename__ = 'dailyTemperatureAndHumidityData'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('station.id'))
    dataType = Column(Enum(EntryType))
    min_reading = Column(Float)
    max_reading = Column(Float)
    date = Column(Date)

    station = relationship('Station')


class authStatus(enum.Enum):
    no_privileges = 'no_privileges'
    low_privileges = 'low_privileges'
    high_privileges = 'high_privileges'

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String, unique=True)
    password = Column(String, nullable=True)
    name = Column(String)
    contact_number = Column(Integer)
    purpose = Column(String)
    #authorized = Column(Enum(authStatus), default=authStatus.no_privileges)
    authorized = Column(String, default= 'no privileges')
    @classmethod
    def get_user(cls, email_id):
       return cls.get(email_id = email_id)

    def verify_password(self, password):
        return bcrypt.verify(password,self.password)

class Units(base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, autoincrement=True)
    measurement = Column(String)
    unit = Column(String)