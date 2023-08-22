from .database import base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Date, Time
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class Garden(base):
    __tablename__ = 'garden'

    g_id = Column(Integer, primary_key=True)
    garden_name = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city_town = Column(String(20), nullable=False)
    state = Column(String(20), nullable=False)
    sizeofgarden = Column(Float, nullable=True)


class Sensor(base):
    __tablename__ = 'sensor'
    sensor_id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sensor_type = Column(String(20), nullable=False)
    sensor_name = Column(String(20), nullable=False)


class SensorReading(base):
    __tablename__ = 'sensorReading'

    entry_id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'), primary_key=True)

    # Define relationships
    sensor = relationship('Sensor')


class GardenAndSensor(base):
    __tablename__ = 'gardenAndSensor'

    sensor_id = Column(Integer, ForeignKey('sensor.sensor_id'), primary_key=True)
    g_id = Column(Integer, ForeignKey('garden.g_id'), primary_key=True)

    garden = relationship('Garden')
    sensor = relationship('Sensor')


class EntryType(PyEnum):
    humidity = 'humidity'
    temperature = 'temperature'


class RainfallData(base):
    __tablename__ = 'rainfallData'

    entry_id = Column(Integer, ForeignKey('sensorReading.entry_id'), primary_key=True)
    reading = Column(Integer)
    date = Column(Date)

    # Establish a relationship with SensorReading
    sensor_reading = relationship("SensorReading")


class TemperatureAndHumidityData(base):
    __tablename__ = 'temperatureAndHumidityData'

    entry_id = Column(Integer, ForeignKey('sensorData.entry_id'), primary_key=True)
    dataType = Column(String(collation='pg_catalog.default'))
    reading = Column(Float)
    time = Column(Time)

    # Establish a relationship with SensorData
    #sensor_data = relationship("SensorData")