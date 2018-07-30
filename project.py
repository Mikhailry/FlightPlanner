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
# session.add(Airport(code='ORD', name="O’Hare International Airport", country='USA', state='IL'))
# session.add(Customer(email='makmoud98@gmail.com', password='pokemon', first_name='Michael', last_name='Elnajami', airport='ORD'))
# session.commit()

# check if email exists
# if not return false
# if so check if password is corrent
# if password is incorrect return false, otherwise return true
def login(email, password):
	exists = session.query(Customer).filter(Customer.email==email).all()
	if not exists:
		print('An account with that email address does not exist.')
		return False
	elif exists[0].password != password:
		print('Incorrect password.')
		return False
	else:
		print('Success!')
		return True

# check if email exists
# if so return false
# otherwise ensure other params are not empty 
# then insert into database
# return true on success
def register(email, first_name, last_name, password, airport):
	exists = session.query(Customer).filter(Customer.email==email).all()
	if exists:
		print('An account with that email address already exists.')
		return False
	elif not first_name or not last_name or not password or not airport:
		print('One or more required fields are missing.')
		return False
	else:
		new_cust = Customer(email=email, first_name=first_name, last_name=last_name, password=password, airport=airport)
		try:
			session.add(new_cust)
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			return False
		print('Success!')
		return True

# check if billing_id already exists
# then return false
# check if address_id is not empty and exists 
# else return false
# check if all other params are not empty
def add_payment(email, billing_id, name, card_no, exp_mo, exp_yr, address_id):
	exists = session.query(CustomerBilling).filter(CustomerBilling.email==email, CustomerBilling.billing_id==billing_id).all()
	if exists:
		print('Billing ID already exists.')
		return False
	elif not billing_id or not name or not card_no or not exp_mo or not exp_yr or not address_id:
		print('One or more required fields are missing.')
		return False
	else:
		new_bill = CustomerBilling(email=email, billing_id=billing_id, name=name, card_no=card_no, exp_mo=exp_mo, exp_yr=exp_yr, address_id=address_id)
		try:
			session.add(new_bill)
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			return False
		print('Success!')
		return True

# check if billing id already exists
# else return false
# check if address_id is not empty and exists 
# else return false
# check if all other params are not empty
def edit_payment(email, billing_id, name, card_no, exp_mo, exp_yr, address_id):
	pass


# just delete
def delete_payment(email, billing_id):
	pass

# check if address_id already exists
# then return false
# check all other non-nulable params
def add_address(email, address_id, name, address_line_1, address_line_2, city, state, zip_code, phone_no):
	exists = session.query(CustomerAddress).filter(CustomerAddress.email==email, CustomerAddress.address_id==address_id).all()
	if exists:
		print('Address ID already exists.')
		return False
	elif not address_id or not name or not address_line_1 or not city or not state or not zip_code or not phone_no:
		print('One or more required fields are missing.')
		return False
	else:
		new_addr = CustomerAddress(email=email, address_id=address_id, name=name, address_line_1=address_line_1, address_line_2=address_line_2, city=city, state=state, zip_code=zip_code, phone_no=phone_no)
		try:
			session.add(new_addr)
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			return False
		print('Success!')
		return True

# check if address_id already exists
# else return false
# check all other non-nulable params
def edit_address(email, address_id, name, address_line_1, address_line_2, city, state, zip_code, phone_no):
	pass

# delete it
def delete_address(email, address_id):
	pass

# ensure that they have enough seats 
# andy wll do ths
# return array of `Flight`s
def find_flights(date, airport_depart, airport_arrival):
	pass

# ensure the flight actually exists 
# ensure that the customer_billing actually exists
# ensure first and last name not blank
# update bonus miles 
# add 1 to the current depending on seat type
def create_booking(email, first_name, last_name, code, flight_no, date, seat_type, billing_id):
	pass

# delete booking
# remove bonus miles
# sub 1 from the current seat
def cancel_booking(booking_id):
	pass

# todo: find a way to do this given 2 airport codes
def calculate_miles(code1, code2):
	pass