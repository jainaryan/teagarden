import enum
from database import base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy import Enum


class Garden(base):
    __tablename__ = 'garden'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    district = Column(String(20), nullable=True)
    state = Column(String(20), nullable=False)
    area = Column(Float, nullable=True)


class Sensor(base):
    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sensor_type = Column(String(50), nullable=True)
    sensor_name = Column(String(50), nullable=True, unique=True)
    garden_id = Column(Integer, ForeignKey('garden.id'), nullable=False)

    # Establish a relationship with Sensor
    garden = relationship('Garden')


class RainfallData(base):
    __tablename__ = 'rainfallData'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    reading = Column(Integer)
    date = Column(Date)

    # Establish a relationship with Sensor
    sensor = relationship('Sensor')


class EntryType(enum.Enum):
    humidity = 'humidity'
    temperature = 'temperature'


class TemperatureAndHumidityData(base):
    __tablename__ = 'temperatureAndHumidityData'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    dataType = Column(Enum(EntryType))
    reading = Column(Float)
    timestamp = Column(Time)
    # Establish a relationship with Sensor
    sensor = relationship('Sensor')

# enum not working
