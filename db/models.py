from sqlalchemy import Column, Integer, Float, DateTime, String
from db.database import Base
from datetime import datetime, UTC

class Prediction(Base):
    __tablename__ =  "predictions"

    id = Column(Integer, primary_key=True, index= True)

    time = Column(Float)
    delay = Column(Float)
    speed = Column(Float)
    distance = Column(Float)
    day = Column(Integer)

    prediction = Column(Float, nullable=True)
    error = Column(Float,nullable=True)
    actual_closing_time = Column(Float,nullable = True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

class RailwayGate(Base):
    __tablename__ = "railway_gates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
