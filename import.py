from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from relations import Base, Customer, CustomerAddress, CustomerBilling, Airport, Airline, Flight, Booking, MileageProgram

import csv
import os.path

# Create an engine to the DB
engine = create_engine('postgresql+psycopg2://'+'dev:cs425'+'@caveofwonders.duckdns.org:5432/' + 'CS425', echo=False) #echo - output all SQL produced

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

#setup session for sqlalchemy
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Import data from 'airport.csv'
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "data/airports.csv")

with open(path, encoding = 'utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')

#Iterate over the rows
    for row in csv_reader:
        session.add(Airport(iata=row[0], name= row[1], country=row[4], state=row[3]))

#commit changes
session.commit()

session = DBSession()
# Import data from 'airlines.csv'
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "data/airlines.csv")

with open(path, encoding = 'utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')

# Iterate over the rows
    for row in csv_reader:
        session.add(Airline(code=row[0], name= row[1], country=row[2]))

#commit changes
session.commit()


# Import data from 'flight_data.csv'
session = DBSession()
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "data/flight_data.csv")

with open(path, encoding = 'utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')

# Iterate over the rows
    for row in csv_reader:
        session.add(Flight(code=row[1], flight_no = row[2], date = row[8], distance = row[6], airport_depart = row[3], airport_arrival = row[4], time_depart = row[5], time_arrival = row[7], seat_max_first = row[9], seat_max_econ = row[10]))

#commit changes
session.commit()
