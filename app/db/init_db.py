from app.db.database import Base, engine
from app.models import models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
