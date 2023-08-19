from sqlapp.database import base
from sqlalchemy import Column, BigInteger, String, ForeignKey, Enum, TIMESTAMP,Integer, Float
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class garden(base):
    __tablename__ = 'garden'

    g_id = Column(Integer, primary_key=True)
    garden_name = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city_town = Column(String(20), nullable=False)
    state = Column(String(20), nullable=False)
    sizeofgarden = Column(Float, nullable=True)


class sensor(base):
    __tablename__ = 'sensor'
    sensor_id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sensor_type = Column(String(20), nullable=False)
    sensor_name = Column(String(20), nullable=False)


class sensorReading(base):
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
    rainfall = 'rainfall'
    humidity = 'humidity'
    temperature = 'temperature'

class TimeframeType(PyEnum):
    immediate_mesaurement = 'immediate measurement'
    range_measurement = 'range_measurement'


class SensorData(base):
    __tablename__ = 'sensorData'

    entry_id = Column(BigInteger, primary_key=True)
    type = Column(Enum(EntryType), nullable=False)
    reading = Column(String(15), nullable=False)
    unit = Column(String(15), nullable=False)
    timeframe = Column(Enum(TimeframeType), nullable=False)
    time = Column(TIMESTAMP, nullable=True)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)

    entry = relationship('SensorReading', back_populates='data')