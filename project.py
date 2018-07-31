import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, aliased
from relations import Base, Customer, CustomerAddress, CustomerBilling,\
					  Airport, Airline, Flight, Booking, MileageProgram

#get connection url
DB_CONN = json.loads(open('database_connection.json', 'r').read())
engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' %  \
                      (DB_CONN['username'], DB_CONN['password'], \
                       DB_CONN['hostname'], str(DB_CONN['port']),\
                       DB_CONN['database']))
#setup session for sqlalchemy
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# session.add(Airport(code='ORD', name="O’Hare International Airport", country='USA', state='IL'))
# session.add(Customer(email='makmoud98@gmail.com', password='pokemon', first_name='Michael', last_name='Elnajami', airport='ORD'))
# session.commit()

# check if email exists
# if not return false
# if so check if password is corrent
# if password is incorrect return false, otherwise return true
def login(email, password):
	session = DBSession()
	exists = session \
			 .query(Customer) \
			 .filter(Customer.email==email) \
			 .first()
	if not exists:
		print('An account with that email address does not exist.')
		session.close()
		return False
	elif exists.password != password:
		print('Incorrect password.')
		session.close()
		return False
	else:
		print('Success!')
		session.close()
		return True

# check if email exists
# if so return false
# otherwise ensure other params are not empty 
# then insert into database
# return true on success
def register(email, first_name, last_name, password, airport):
	session = DBSession()
	exists = session \
			 .query(Customer) \
			 .filter(Customer.email==email) \
			 .first()
	if exists:
		print('An account with that email address already exists.')
		session.close()
		return False
	elif not first_name or not last_name or not password or not airport:
		print('One or more required fields are missing.')
		session.close()
		return False
	else:
		new_cust = Customer(email=email, first_name=first_name,
							last_name=last_name, password=password,
							airport=airport)
		try:
			session.add(new_cust)
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# check if address_id already exists
# then return false
# check all other non-nulable params
def add_address(email, address_id, name, address_line_1, address_line_2,
				city, state, zip_code, phone_no):
	session = DBSession()
	exists = session \
			 .query(CustomerAddress) \
			 .filter(CustomerAddress.email==email,
			 		 CustomerAddress.address_id==address_id) \
			 .first()
	if exists:
		print('Address ID already exists.')
		session.close()
		return False
	elif not address_id or not name or not address_line_1 or not city \
	or not state or not zip_code or not phone_no:
		print('One or more required fields are missing.')
		session.close()
		return False
	else:
		new_addr = CustomerAddress(email=email, address_id=address_id,
								   name=name,
								   address_line_1=address_line_1,
								   address_line_2=address_line_2,
								   city=city, state=state,
								   zip_code=zip_code, phone_no=phone_no)
		try:
			session.add(new_addr)
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# check if address_id already exists
# else return false
# check all other non-nulable params
def edit_address(email, address_id, name, address_line_1,
				 address_line_2, city, state, zip_code, phone_no):
	session = DBSession()
	exists = session \
			 .query(CustomerAddress) \
			 .filter(CustomerAddress.email==email,
    				 CustomerAddress.address_id==address_id) \
			 .first()
	if not exists:
		print('Address ID does not exist.')
		session.close()
		return False
	elif not address_id or not name or not address_line_1 or not city\
	or not state or not zip_code or not phone_no:
		print('One or more required fields are missing.')
		session.close()
		return False
	else:
		try:
			session \
			.query(CustomerAddress) \
			.filter(CustomerAddress.email==email,
				    CustomerAddress.address_id==address_id) \
			.update({CustomerAddress.name: name,
				     CustomerAddress.address_line_1: address_line_1,
					 CustomerAddress.address_line_2: address_line_2,
					 CustomerAddress.city: city,
					 CustomerAddress.state: state,
					 CustomerAddress.zip_code: zip_code,
					 CustomerAddress.phone_no: phone_no})
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# delete it
def delete_address(email, address_id):
	session = DBSession()
	exists = session \
			 .query(CustomerAddress) \
			 .filter(CustomerAddress.email==email,
			 		 CustomerAddress.address_id==address_id) \
			 .first()
	if not exists:
		print('Address ID does not exist.')
		session.close()
		return False
	else:
		try:
			session \
			 .query(CustomerAddress) \
			 .filter(CustomerAddress.email==email,
			 		 CustomerAddress.address_id==address_id) \
			 .delete()
			session.commit()
		except:
			print('Issue committing to database')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# check if billing_id already exists
# then return false
# check if address_id is not empty and exists 
# else return false
# check if all other params are not empty
def add_payment(email, billing_id, name, card_no, exp_mo, exp_yr,
				address_id):
	session = DBSession()
	exists = session \
			 .query(CustomerBilling) \
			 .filter(CustomerBilling.email==email,
			 		 CustomerBilling.billing_id==billing_id) \
			 .first()
	if exists:
		print('Billing ID already exists.')
		session.close()
		return False
	elif not billing_id or not name or not card_no or not exp_mo \
	or not exp_yr or not address_id:
		print('One or more required fields are missing.')
		session.close()
		return False
	else:
		new_billing = CustomerBilling(email=email,
									  billing_id=billing_id, name=name,
									  card_no=card_no, exp_mo=exp_mo,
									  exp_yr=exp_yr,
									  address_id=address_id)
		try:
			session.add(new_billing)
			session.commit()
		except:
			print('Issue committing to database.')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# check if billing id already exists
# else return false
# check if address_id is not empty and exists 
# else return false
# check if all other params are not empty
def edit_payment(email, billing_id, name, card_no, exp_mo, exp_yr,
				 address_id):
	session = DBSession()
	exists = session \
			 .query(CustomerBilling) \
			 .filter(CustomerBilling.email==email,
			 		 CustomerBilling.billing_id==billing_id) \
			 .first()
	if not exists:
		print('Billing ID does not exist.')
		session.close()
		return False
	elif not billing_id or not name or not card_no or not exp_mo \
	or not exp_yr or not address_id:
		print('One or more required fields are missing.')
		session.close()
		return False
	else:
		try:
			session \
			.query(CustomerBilling) \
			.filter(CustomerBilling.email==email,
				    CustomerBilling.billing_id==billing_id) \
			.update({CustomerBilling.name: name,
				     CustomerBilling.card_no: card_no,
					 CustomerBilling.exp_mo: exp_mo,
					 CustomerBilling.exp_yr: exp_yr,
					 CustomerBilling.address_id: address_id})
			session.commit()
		except:
			print('Issue committing to database')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# just delete
def delete_payment(email, billing_id):
	session = DBSession()
	exists = session \
			 .query(CustomerBilling) \
			 .filter(CustomerBilling.email==email,
			 		 CustomerBilling.billing_id==billing_id) \
			 .first()
	if not exists:
		print('Billing ID does not exist.')
		session.close()
		return False
	else:
		try:
			session.delete(exists)
			session.commit()
		except:
			print('Issue committing to database')
			session.rollback()
			session.close()
			return False
		print('Success!')
		session.close()
		return True

# ensure that they have enough seats 
# andy wll do ths
# return array of `Flight`s
def find_flights(date, airport_depart, airport_arrival, max_stops):
	session = DBSession()
	query1 =  "select * \
	  		   from flight \
			   where date == :date \
				 and airport_depart == :airport_depart \
				 and airport_arrive == :airport_arrive \
				 and (seat_current_first < seat_max_first \
				      or seat_current_econ < seat_max_econ) \
				 and :max_stops == 0"
	query2 = "select * \
			  from flight flight1, flight flight2 \
			  where flight1.date == :date \
				and flight1.airport_depart == :airport_depart \
			    and flight2.airport_arrive == :airport_arrive \
				and flight2.time_depart - flight1.time_arrive > [30min] \
				and flight2.time_arrive - flight1.time_depart < [24hrs] \
				and (flight1.seat_current_first < flight1.seat_max_first \
				     or flight1.seat_current_econ < flight1.seat_max_econ) \
				and (flight2.seat_current_first < flight2.seat_max_first \
				     or flight2.seat_current_econ < flight2.seat_max_econ) \
				and :max_stops == 1"
	query3 = "select * \
			  from flight flight1, flight flight2, flight flight3 \
			  where flight1.date == :date \
			    and flight1.airport_depart == :airport_depart \
			    and flight2.airport_arrive == flight1.airport_depart \
			    and flight3.airport_arrive == :airport_arrive \
			    and flight2.time_depart - flight1.time_arrive > [30min] \
			    and flight3.time_depart > flight2.time_arrive > [30min] \
			    and flight3.time_arrive - flight1.time_depart < [48hrs] \
			    and (flight1.seat_current_first < flight1.seat_max_first \
			         or flight1.seat_current_econ < flight1.seat_max_econ) \
			    and (flight2.seat_current_first < flight2.seat_max_first \
			  	     or flight2.seat_current_econ < flight2.seat_max_econ) \
			    and (flight3.seat_current_first < flight3.seat_max_first \
			  	     or flight3.seat_current_econ < flight3.seat_max_econ) \
			    and :max_stops == 2"
	depart_exists = session \
			        .query(Airport) \
			        .filter(Airport.code==airport_depart) \
			        .all()
	if not depart_exists:
		print('Departure airport does not exist.')
		session.close()
		return False
	arrive_exists = session \
					.query(Airport) \
					.filter(Airport.code==airport_depart) \
					.all()
	if not arrive_exists:
		print('Arrival airport does not exist.')
		session.close()
		return False
	if max_stops == 0:
		flights = session \
		  		  .query(Flight) \
		  		  .from_statement(text(query1)) \
		  		  .params(date=date, airport_depart=airport_depart,
		  		  	      airport_arrive=airport_arrive,
		  		  	      max_stops=max_stops) \
				  .all()
		if not flights:
			print('No flights found with the given criteria.')
			session.close()
			return False
		else:
			print('Success!')
			session.close()
			return flights
	elif max_stops == 1:
		
		flights1 = session \
		  		   .query(Flight1) \
		  		   .from_statement(text(query1)) \
		  		   .params(date=date, airport_depart=airport_depart,
		  		   	       airport_arrive=airport_arrive,
		  		  	       max_stops=max_stops) \
				   .all()
		flights2 = session \
		  		   .query(Flight) \
		  		   .from_statement(text(query2)) \
		  		   .params(date=date, airport_depart=airport_depart,
		  		   	       airport_arrive=airport_arrive,
		  		  	       max_stops=max_stops) \
				   .all()
		if not flights1 and not flights2:
			print('No flights found with the given criteria.')
			session.close()
			return False
		else:
			print('Success!')
			session.close()
			return flights1, flights2
	elif max_stops == 2:
		flights1 = session \
		  		   .query(Flight1) \
		  		   .from_statement(text(query1)) \
		  		   .params(date=date, airport_depart=airport_depart,
		  		   	       airport_arrive=airport_arrive,
		  		  	       max_stops=max_stops) \
				   .all()
		flights2 = session \
		  		   .query(Flight) \
		  		   .from_statement(text(query2)) \
		  		   .params(date=date, airport_depart=airport_depart,
		  		   	       airport_arrive=airport_arrive,
		  		  	       max_stops=max_stops) \
				   .all()
		flights3 = session \
		  		   .query(Flight) \
		  		   .from_statement(text(query3)) \
		  		   .params(date=date, airport_depart=airport_depart,
		  		   	       airport_arrive=airport_arrive,
		  		  	       max_stops=max_stops) \
				   .all()
		if not flights1 and not flights2 and not flights3:
			print('No flights found with the given criteria.')
			session.close()
			return False
		else:
			print('Success!')
			session.close()
			return flights1, flights2, flights3
	else:
		print('Up to two stops are permitted in an itinerary.')
		session.close()
		return False

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