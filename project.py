import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from relations import Base, Customer, CustomerAddress, CustomerBilling, Airport, Airline, Flight, Booking, MileageProgram

#get connection url
DB_CONN = json.loads(open('database_connection.json', 'r').read())
engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' %  \
                      (DB_CONN['username'], DB_CONN['password'], \
                       DB_CONN['hostname'], str(DB_CONN['port']),\
                       DB_CONN['database']))
#setup session for sqlalchemy
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add(Airport(iata='ORD', name="O’Hare International Airport", country='USA', state='IL'))
session.add(Customer(email='makmoud98@gmail.com', password='pokemon', first_name='Michael', last_name='Elnajami', airport='ORD'))
session.commit()

# check if email exists
# if not return false
# if so check if password is corrent
# if password is incorrect return false, otherwise return true
def login(email, password):

# check if email exists
# if so return false
# otherwise ensure other params are not empty 
# then insert into database
# return true on success
def register(email, first_name, last_name, password, airport)

# check if billing_id already exists
# then return false
# check if address_id is not empty and exists 
# else return false
# check if all other params are not empty
def add_payment(email, billing_id, name, card_no, exp_mo, exp_yr, address_id)

# check if billing id already exists
# else return false
# check if address_id is not empty and exists 
# else return false
# check if all other params are not empty
def edit_payment(email, billing_id, name, card_no, exp_mo, exp_yr, address_id)

# just delete
def delete_payment(email, billing_id)

# check if address_id already exists
# then return false
# check all other non-nulable params
def add_address(email, address_id, name, address_line_1, address_line_2, city, state, zip_code, phone_no)

# check if address_id already exists
# else return false
# check all other non-nulable params
def edit_address(email, address_id, name, address_line_1, address_line_2, city, state, zip_code, phone_no)

# delete it
def delete_address(email, address_id)

# ensure that they have enough seats 
# andy wll do ths
# return array of `Flight`s
def find_flights(date, airport_depart, airport_arrival)

# ensure the flight actually exists 
# ensure that the customer_billing actually exists
# ensure first and last name not blank
# update bonus miles 
# add 1 to the current depending on seat type
def create_booking(email, first_name, last_name, code, flight_no, date, seat_type, billing_id)

# delete booking
# remove bonus miles
# sub 1 from the current seat
def cancel_booking(booking_id)

# todo: find a way to do this given 2 airport codes
def calculate_miles(code1, code2)