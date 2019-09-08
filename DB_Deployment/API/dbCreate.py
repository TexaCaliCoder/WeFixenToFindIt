from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite///:DB_Deployment/API/mapData.db', echo = True)
Base = declarative_base()

class Room(Base):
    __tablename__ = "room"

    id = Column( 'id', Integer, primary_key=True)
    coordinates = Column('coordinates', String)
    name = Column('name', String)
    description = Column('description', String)
    n = ('n', String)
    s = ('s', String)
    e = ('e', String)
    w = ('w', String)

Base.metadata.create_all(bind=engine)