from database import SessionLocal
from models import Prediction
from models import RailwayGate
db = SessionLocal()

sample_data = [
    {"time":12, "delay":10, "speed":60, "distance":5, "day":2},
    {"time":18, "delay":5, "speed":80, "distance":3, "day":4},
    {"time":9, "delay":0, "speed":50, "distance":7, "day":1},
]

for data in sample_data:
    actual = (data["distance"] / data["speed"]) * 60 + data["delay"] - 2
    record = Prediction(**data, actual_closing_time=actual)
    db.add(record)

db.commit()
db.close()

print("Data inserted")

db = SessionLocal()
gates = [
    RailwayGate(name="Gate A", latitude=18.5204, longitude=73.8567),
    RailwayGate(name="Gate B", latitude=18.5310, longitude=73.8440),
    RailwayGate(name="Gate C", latitude=18.5100, longitude=73.8700),
]

db.add_all(gates)
db.commit()
db.close()

print("Gates Inserted")