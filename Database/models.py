from sqlalchemy import Column, Integer, Float, DateTime
from database import Base
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
    actual_closing_time = Column(Float,nullable = True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))