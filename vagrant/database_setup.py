import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Classes
# Shelter Class
class Shelter(Base):
    __tablename__ = 'shelter'

    name = Column(
        String(80), nullable=False
    )
    address = Column(
        String(256), nullable=False
    )
    city = Column(
        String(20), nullable=False
    )
    state = Column(
        String(20), nullable=False
    )
    zipCode = Column(
        Integer, nullable=False
    )
    website = Column(
        String(80)
    )
    id = Column(
        Integer, primary_key=True
    )


# Puppy Class
class Puppy(Base):
    __tablename__ = 'puppy'

    name = Column(
        String(80), nullable=False
    )
    id = Column(
        Integer, primary_key=True
    )
    date_of_birth = Column(
        Date
    )
    gender = Column(
        String(6), nullable=False
    )
    weight = Column(
        Float
    )
    shelter_id = Column(
        Integer, ForeignKey(Shelter.id)
    )
    shelter = relationship(Shelter)


# End of the file
engine = create_engine(
    'sqlite:///shelterpuppy.db'
)

Base.metadata.create_all(engine)
