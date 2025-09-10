import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))
if not database_exists(engine.url):
    create_database(engine.url)

Base = declarative_base()

class Biodata(Base):
    __tablename__ = "biodata"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(15))
    last_name = Column(String(15))
    age = Column(Integer)
    state_of_origin = Column(String(15))
    country = Column(String, default="NGA")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "state_of_origin": self.state_of_origin,
            "country": self.country
        }

Base.metadata.create_all(bind=engine)
db_session = sessionmaker(bind=engine)
session = db_session()
