from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Date, DateTime, CHAR 
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import json

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    email       = Column(String(50), primary_key=True, index=True)
    password    = Column(String(50), nullable=False)
    first_name  = Column(String(50), nullable=False)
    last_name   = Column(String(50), nullable=False)
    airport     = Column(CHAR(3), ForeignKey('airport.code'), nullable=False)

class CustomerAddress(Base):
    __tablename__ = 'customer_address'

    email       = Column(String(50), ForeignKey('customer.email'), primary_key=True)
    address_id  = Column(String(20), primary_key=True)
    name        = Column(String(100), nullable=False)
    address_line_1  = Column(String(20), nullable=False)
    address_line_2  = Column(String(20))
    city        = Column(String(50), nullable=False)
    state       = Column(CHAR(2), nullable=False)
    zip_code    = Column(String(10), nullable=False)
    phone_no    = Column(String(15), nullable=False)

class CustomerBilling(Base):
    __tablename__ = 'customer_billing'

    email       = Column(String(50), primary_key=True)
    billing_id  = Column(String(20), primary_key=True, nullable=False)
    name        = Column(String(100), nullable=False)
    card_no     = Column(String(16), nullable=False)
    exp_mo      = Column(CHAR(2), nullable=False)
    exp_yr      = Column(CHAR(2), nullable=False)
    address_id  = Column(String(20), nullable=False)

    __table_args__ = ( ForeignKeyConstraint(['email', 'address_id'], ['customer_address.email', 'customer_address.address_id']),)

class Airport(Base):
    __tablename__ = 'airport'

    code        = Column(CHAR(3), primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    country     = Column(String(50), nullable=False)
    state       = Column(CHAR(2))

class Airline(Base):
    __tablename__ = 'airline'

    code        = Column(CHAR(2), primary_key=True, index=True)
    name        = Column(String(50), nullable=False)
    country     = Column(String(50), nullable=False)

class Flight(Base):
    __tablename__ = 'flight'

    code        = Column(CHAR(2), ForeignKey('airline.code'), primary_key=True)
    flight_no   = Column(String(4), primary_key=True, nullable=False)
    date        = Column(Date, nullable=False)
    distance    = Column(Integer, nullable=False)
    airport_depart  = Column(CHAR(3), ForeignKey('airport.code'), nullable=False)
    airport_arrival = Column(CHAR(3), ForeignKey('airport.code'), nullable=False)
    time_depart = Column(DateTime, primary_key=True, nullable=False)
    time_arrival= Column(DateTime, nullable=False)
    seat_max_first  = Column(Integer, nullable=False)
    seat_max_econ   = Column(Integer, nullable=False)
    seat_current_first  = Column(Integer, nullable=False, default=0)
    seat_current_econ   = Column(Integer, nullable=False, default=0)

class Booking(Base):
    __tablename__ = 'booking'

    booking_id  = Column(Integer, primary_key=True)
    email       = Column(String(50), primary_key=True)
    first_name  = Column(String(50), primary_key=True)
    last_name   = Column(String(50), primary_key=True)
    code        = Column(CHAR(2), primary_key=True)
    flight_no   = Column(String(4), primary_key=True)
    time_depart = Column(DateTime, primary_key=True)
    seat_type   = Column(String(5), nullable=False)
    billing_id  = Column(String(20), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['code', 'flight_no', 'time_depart'], ['flight.code', 'flight.flight_no', 'flight.time_depart']),\
                      ForeignKeyConstraint(['email', 'billing_id'], ['customer_billing.email', 'customer_billing.billing_id']))


class MileageProgram(Base):
    __tablename__ = 'mileage_program'

    email       = Column(String(50), ForeignKey('customer.email'), primary_key=True)
    code        = Column(CHAR(2), ForeignKey('airline.code'), primary_key=True)
    bonus_miles = Column(Integer, default=0)


DB_CONN = json.loads(open('database_connection.json', 'r').read())
engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' %  \
                      (DB_CONN['username'], DB_CONN['password'], \
                       DB_CONN['hostname'], str(DB_CONN['port']),\
                       DB_CONN['database']))
Base.metadata.create_all(engine)
