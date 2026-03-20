from database import engine
from Database.models import Base

Base.metadata.create_all(bind=engine)
print("Table create successfully")
