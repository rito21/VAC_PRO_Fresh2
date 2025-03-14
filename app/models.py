from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "db_empresa"
    id = Column(Integer, primary_key=True, index=True)
    nom_empresa = Column(String(100), unique=True, nullable=False)
    usuaris = relationship("Usuari", back_populates="empresa")

class Usuari(Base):
    __tablename__ = "db_usuari"
    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    correu_electronic = Column(String(100), unique=True, nullable=False)
    contrasenya = Column(String(255), nullable=False)  # Aumenté a 255 para hashes largos
    data_registre = Column(DateTime, default=datetime.utcnow)
    ultim_canvi_contrasenya = Column(DateTime, default=datetime.utcnow)
    intents_fallits_login = Column(Integer, default=0)
    bloquejat = Column(Boolean, default=False)
    baixa = Column(Boolean, default=False)
    compte_verificat = Column(Boolean, default=False)
    nom = Column(String(50), nullable=False)
    cognoms = Column(String(50), nullable=False)
    empresa = relationship("Empresa", back_populates="usuaris")
    devices = relationship("Device", back_populates="usuari")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    id_usuari = Column(Integer, ForeignKey("db_usuari.id"), nullable=False)
    usuari = relationship("Usuari", back_populates="devices")

class TipusSensor(Base):
    __tablename__ = "tbl_tipus_sensor"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), unique=True, nullable=False)
    descripcio = Column(String)
    unitat = Column(String(20), nullable=False)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    sensors = relationship("Sensor", back_populates="tipus_sensor")

class EstacioMeteo(Base):
    __tablename__ = "tbl_estacio_meteo"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    descripcio = Column(String)
    ubicacio = Column(String(255))
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    ultima_connexio = Column(DateTime)
    ip_address = Column(String(45))
    mac_address = Column(String(17), unique=True)
    versio_firmware = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    sensors = relationship("Sensor", back_populates="estacio")

class Sensor(Base):
    __tablename__ = "tbl_sensor"
    id = Column(Integer, primary_key=True, index=True)
    id_estacio = Column(Integer, ForeignKey("tbl_estacio_meteo.id"), nullable=False)
    id_tipus_sensor = Column(Integer, ForeignKey("tbl_tipus_sensor.id"), nullable=False)
    nom = Column(String(50), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    ultima_lectura = Column(DateTime)
    calibracio = Column(String)  # JSONB en la base de datos
    estacio = relationship("EstacioMeteo", back_populates="sensors")
    tipus_sensor = relationship("TipusSensor", back_populates="sensors")
    measurements = relationship("Measurement", back_populates="sensor")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    id_sensor = Column(Integer, ForeignKey("tbl_sensor.id"), nullable=False)
    sensor = relationship("Sensor", back_populates="measurements")