from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
 
class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    forecasts = relationship("Forecast", back_populates="location")

class Forecast(Base):
    __tablename__ = 'forecasts'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    forecast_date = Column(Date)
    the_temp = Column(Float)
    wind_speed = Column(Float)
    precipitation = Column(Float)

    location = relationship("Location", back_populates="forecasts")

engine = create_engine('sqlite:///weather.db')  
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
