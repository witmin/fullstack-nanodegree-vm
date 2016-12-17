from sqlalchemy import create_engine, asc,  desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy

engine = create_engine('sqlite:///shelterpuppy.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# ****** Add data
# shelterOne = Shelter(name="A Shelter 1", address="HK", city="HK", state="HK", zipCode=0, id=4)
# session.add(shelterOne)
#
# shelterTwo = Shelter(name="B Shelter 2", address="HK", city="HK", state="HK", zipCode=0, id=2)
# session.add(shelterTwo)
#
# shelterThree = Shelter(name="C Shelter 3", address="HK", city="HK", state="HK", zipCode=0, id=3)
# session.add(shelterThree)
#
# puppyOne = Puppy(name="Tom", id=1, gender='female', weight="2.5", shelter_id=4)
# session.add(puppyOne)
#
# puppyTwo = Puppy(name="Birdy", id=2, gender='female', weight="6", shelter_id=3)
# session.add(puppyTwo)
#
# puppyThree = Puppy(name="Twitter", id=3, gender='male', weight="6", shelter_id=2)
# session.add(puppyThree)

# puppyFour = Puppy(name="Dada", id=4, gender='male', weight="4.3", shelter_id=2)
# session.add(puppyFour)
# session.commit()

# ****** Update
# dada = session.query(Puppy).filter_by(name='Dada').one()
# dada.weight = 4.3
# session.commit()


# ****** Read
all_shelters = session.query(Shelter).all()

for shelter in all_shelters:
    print(shelter.name, '\n', "Shelter id: ", shelter.id)

# all_puppies = session.query(Puppy).order_by(asc(Puppy.name)).all()
# all_puppies = session.query(Puppy).order_by(asc(Puppy.weight)).all()

all_puppies = session.query(Puppy).group_by(Puppy.shelter_id).all()


for puppy in all_puppies:
    print('Puppy name: ', puppy.name, '\n', 'weight:', puppy.weight, 'kg', '\n', 'shelter_id', puppy.shelter_id)
