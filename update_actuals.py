from Database.database import SessionLocal
from Database.models import Prediction

db = SessionLocal()

rows = db.query(Prediction).filter(Prediction.actual_closing_time.is_(None)).all()

print("Rows found:", len(rows))

for r in rows:
    print("Processing row:", r.id)

    actual = (r.distance / r.speed) * 60 + r.delay - 2

    r.actual_closing_time = actual
    r.error = actual - r.prediction

db.commit()
db.close()

print("Update done")