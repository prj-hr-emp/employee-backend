from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)  # No connect_args needed for MySQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()