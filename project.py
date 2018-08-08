import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

DB_CONN = json.loads(open('database_connection.json', 'r').read())
engine = create_engine('postgresql://%s:%s@%s:%s/%s' %
                      (DB_CONN['username'], DB_CONN['password'],
                       DB_CONN['hostname'], str(DB_CONN['port']),
                       DB_CONN['database']))

def login(email, password):
    """
    Validates login credentials

    :returns: True if matching email/password combination found in
              table 'customer', False otherwise.
    """
    sql = text(("select * "
                "from customer "
                "where email = :email and password = :password"))
    with engine.connect() as conn:
        result = conn.execute(sql, {'email': email,
                                    'password': password})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        print('That email/password combination is invalid.')
        return False
    else:
        print('Success!')
        return resultSet[0]

def register(email, first_name, last_name, password, airport):
    """
    Inserts a new row into the 'customer' table

    :returns: True if the new user credentials are complete, unique,
              and do not violate table 'customer' integrity constraints,
              False otherwise or if the insert operation failed.
    """
    sql = text(("select email "
                "from customer "
                "where email = :email"))
    with engine.connect() as conn:
        result = conn.execute(sql, {'email': email})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if resultSet:
        print('An account with that email address already exists.')
        return False
    elif not first_name or not last_name or not password or not airport:
        print('One or more required fields are missing.')
        return False
    else:
        sql = text(("insert into customer "
                    "values(:email, :password, :first_name, "
                    ":last_name, :airport)"))
        try:
            with engine.connect() as conn:
                conn.execute(sql, {'email': email,
                                   'first_name': first_name,
                                   'last_name': last_name,
                                   'password': password,
                                   'airport': airport})
            conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def get_airports():
    """
    Validates login credentials

    :returns: True if matching email/password combination found in
              table 'customer', False otherwise.
    """
    sql = text(("select * "
                "from airport "))
    with engine.connect() as conn:
        result = conn.execute(sql)
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        return False
    else:
        return resultSet

def get_flights(airport_depart, airport_arrival, date):
    """
    Validates login credentials

    :returns: True if matching email/password combination found in
              table 'customer', False otherwise.
    """
    sql = text(("select time_depart "
                "from airport "
                "where airport_depart = :airport_depart and "
                "airport_arrival = :airport_arrival and "
                "date(time_depart) = :date"))
    with engine.connect() as conn:
        result = conn.execute(sql, {"airport_depart": airport_depart,
                                    "airport_arrival": airport_arrival,
                                    "date": date})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        return False
    else:
        return resultSet

def get_billing(email):
    """
    Validates login credentials

    :returns: True if matching email/password combination found in
              table 'customer', False otherwise.
    """
    sql = text(("select billing_id "
                "from customer_billing "
                "where email = :email"))
    with engine.connect() as conn:
        result = conn.execute(sql, {"email": email})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    return resultSet

def add_address(email, address_id, name, address_line_1, address_line_2,
                city, state, zip_code, phone_no):
    """
    Checks to see if the given email/address_id combination exists; if
    not, inserts the row into the 'customer_address' table.

    :returns: True if the new address fields are complete and unique,
              False otherwise or if the insert operation fails.
    """
    sql = text(("select email, address_id "
                "from customer_address "
                "where email = :email and address_id = :address_id"))
    with engine.connect() as conn:
        result = conn.execute(sql, {'email': email,
                                    'address_id': address_id})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if resultSet:
        print('An address with that ID already exists.')
        return False
    elif not address_id or not name or not address_line_1 or not city \
    or not state or not zip_code or not phone_no:
        print('One or more required fields are missing.')
        conn.close()
        return False
    else:
        sql = text(("insert into customer_address "
                    "values(:email, :address_id, :name, "
                    ":address_line_1, :address_line_2, :city, :state, "
                    ":zip_code, :phone_no)"))
        try:
            with engine.connect() as conn:
                conn.execute(sql, {'email': email,
                                   'address_id': address_id,
                                   'name': name,
                                   'address_line_1': address_line_1,
                                   'address_line_2': address_line_2,
                                   'city': city,
                                   'state': state,
                                   'zip_code': zip_code,
                                   'phone_no': phone_no})
            conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def edit_address(email, address_id, name, address_line_1,
                 address_line_2, city, state, zip_code, phone_no):
    """
    Checks to see if the given email/address_id combination exists; if
    so, updates the row in the 'customer_address' table.

    :returns: True if the new address fields are complete, unique, and
              do not violate table 'customer_address' integrity
              constraints, False otherwise or if the update operation
              fails.
    """
    sql = text(("select email, address_id "
                "from customer_address "
                "where email = :email and address_id = :address_id"))
    with engine.connect() as conn:
        result = conn.execute(sql, {'email': email,
                                    'address_id': address_id})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        print('An address with that ID does not exist.')
        return False
    elif not name or not address_line_1 or not city or not state \
    or not zip_code or not phone_no:
        print('One or more required fields are missing.')
        conn.close()
        return False
    else:
        sql = text(("update customer_address "
                    "set name = :name, "
                    "address_line_1 = :address_line_1, "
                    "address_line_2 = :address_line_2, "
                    "city = :city, state = :state, "
                    "zip_code = :zip_code, phone_no = :phone_no "
                    "where email = :email and "
                    "address_id = :address_id"))
        try:
            with engine.connect() as conn:
                conn.execute(sql, {'email': email,
                                   'address_id': address_id,
                                   'name': name,
                                   'address_line_1': address_line_1,
                                   'address_line_2': address_line_2,
                                   'city': city,
                                   'state': state,
                                   'zip_code': zip_code,
                                   'phone_no': phone_no})
                conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def delete_address(email, address_id):
    """
    Checks to see if the given email/address_id combination exists; if
    so, deletes the row in the 'customer_address' table assuming no
    integrity constraints of 'customer_billing' are violated.

    :returns: True if the row is deleted successfully, False if the
              table 'customer_billing' integrity constraints are
              violated upon deletion or if the delete operation fails.
    """
    sql = text(("select email, address_id "
                "from customer_address "
                "where email = :email and address_id = :address_id"))
    with engine.connect() as conn:
        result = conn.execute(sql, {'email': email,
                                    'address_id': address_id})
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        print('An address with that ID does not exist.')
        return False
    else:
        sql = text(("delete from customer_address "
                    "where email = :email and "
                    "address_id = :address_id"))
        try:
            with engine.connect() as conn:
                conn.execute(sql, {'email': email,
                                   'address_id': address_id})
                conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def add_payment(email, billing_id, name, card_no, exp_mo, exp_yr,
                address_id):
    """
    Checks to see if the given email/billing_id combination exists; if
    not, inserts the row into the 'customer_billing' table.

    :returns: True if the new billing fields are complete and unique,
              False otherwise or if the insert operation fails.
    """
    sql = text(("select email, billing_id "
                "from customer_billing "
                "where email = :email and billing_id = :billing_id"))
    keys = {'email': email, 'billing_id': billing_id}
    with engine.connect() as conn:
        result = conn.execute(sql, keys)
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if resultSet:
        print('A billing entry with that ID already exists.')
        return False
    elif not billing_id or not name or not card_no or not exp_mo \
    or not exp_yr or not address_id:
        print('One or more required fields are missing.')
        conn.close()
        return False
    else:
        sql = text(("insert into customer_billing "
                    "values(:email, :billing_id, :name, :card_no, "
                    ":exp_mo, :exp_yr, :address_id)"))
        keys = {'email': email, 'billing_id': billing_id, 'name': name,
                'card_no': card_no, 'exp_mo': exp_mo, 'exp_yr': exp_yr,
                'address_id': address_id}
        try:
            with engine.connect() as conn:
                conn.execute(sql, keys)
            conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def edit_payment(email, billing_id, name, card_no, exp_mo, exp_yr,
                 address_id):
    """
    Checks to see if the given email/billing_id combination exists; if
    so, updates the row in the 'customer_billing' table.

    :returns: True if the new billing fields are complete and unique,
              False otherwise or if the update operation fails.
    """
    sql = text(("select email, billing_id "
                "from customer_billing "
                "where email = :email and billing_id = :billing_id"))
    keys = {'email': email, 'billing_id': billing_id}
    with engine.connect() as conn:
        result = conn.execute(sql, keys)
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        print('A billing entry with that ID does not exist.')
        return False
    elif not name or not card_no or not exp_mo or not exp_yr \
    or not address_id:
        print('One or more required fields are missing.')
        conn.close()
        return False
    else:
        sql = text(("update customer_billing "
                    "set name = :name, card_no = :card_no, "
                    "exp_mo = :exp_mo, exp_yr = :exp_yr, "
                    "address_id = :address_id "
                    "where email = :email and "
                    "billing_id = :billing_id"))
        keys = {'email': email, 'billing_id': billing_id,
                'name': name, 'card_no': card_no, 'exp_mo': exp_mo,
                'exp_yr': exp_yr, 'address_id': address_id}
        try:
            with engine.connect() as conn:
                conn.execute(sql, keys)
                conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def delete_payment(email, billing_id):
    """
    Checks to see if the given email/billing_id combination exists; if
    so, deletes the row in the 'customer_billing' table.

    :returns: True if the row is deleted successfully, False if the
              delete operation fails.
    """
    sql = text(("select email, billing_id "
                "from customer_billing "
                "where email = :email and billing_id = :billing_id"))
    keys = {'email': email, 'billing_id': billing_id}
    with engine.connect() as conn:
        result = conn.execute(sql, keys)
        conn.close()
    resultSet = []
    for row in result:
        resultSet.append(row[0:])
    if not resultSet:
        print('A billing entry with that ID does not exist.')
        return False
    else:
        sql = text(("delete from customer_billing "
                    "where email = :email and "
                    "billing_id = :billing_id"))
        try:
            with engine.connect() as conn:
                conn.execute(sql, keys)
                conn.close()
            print('Success!')
            return True
        except:
            print('Issue committing to database.')
            conn.close()
            return False

def find_flights(date, airport_depart, airport_arrival, max_stops):
    """
    Searches for a path from airport_depart to airport_arrival based on
    how many layover stops are allowed. Each layover has the hard-coded
    constraint of having a minimum duration of 30 minutes and a maximum
    duration of 24 hours.

    :returns: List(s) of matching flights if any are found, False
              otherwise.
    """
    sql0 =  text(("select flight.code, flight.flight_no, "
                  "airport_depart, airport_arrival, "
                  "flight.time_depart, time_arrival, type, price "
                  "from flight, seat "
                  "where flight.code = seat.code and "
                  "flight.flight_no = seat.flight_no and "
                  "flight.time_depart = seat.time_depart and "
                  "date(flight.time_depart) = :date and "
                  "airport_depart = :airport_depart and "
                  "airport_arrival = :airport_arrival and "
                  "current < max"))
    sql1 = text(("select F1.code, F1.flight_no, "
                 "F1.airport_depart, F1.airport_arrival, "
                 "F1.time_depart, F1.time_arrival, F2.code, "
                 "F2.flight_no, F2.airport_depart, "
                 "F2.airport_arrival, F2.time_depart, "
                 "F2.time_arrival, S1.type, S2.type, "
                 "S1.price + S2.price total_price "
                 "from flight F1, flight F2, seat S1, seat S2 "
                 "where F1.code = S1.code and "
                 "F1.flight_no = S1.flight_no and "
                 "F1.time_depart = S1.time_depart and "
                 "F2.code = S2.code and "
                 "F2.flight_no = S2.flight_no and "
                 "F2.time_depart = S2.time_depart and "
                 "date(F1.time_depart) = :date and "
                 "F1.airport_depart = :airport_depart and "
                 "F1.airport_arrival = F2.airport_depart and "
                 "F2.airport_arrival = :airport_arrival and "
                 "F2.time_depart > F1.time_arrival + interval "
                 "\'30 minutes\' and "
                 "F2.time_depart < F1.time_arrival + interval "
                 "\'1 day\' and "
                 "S1.current < S1.max and "
                 "S2.current < S2.max"))
    sql2 = text(("select F1.code, F1.flight_no, "
                 "F1.airport_depart, F1.airport_arrival, "
                 "F1.time_depart, F1.time_arrival, F2.code, "
                 "F2.flight_no, F2.airport_depart, "
                 "F2.airport_arrival, F2.time_depart, "
                 "F2.time_arrival, F3.code, F3.flight_no, "
                 "F3.airport_depart, F3.airport_arrival, "
                 "F3.time_depart, F3.time_arrival, S1.type, S2.type, "
                 "S3.type, S1.price + S2.price + S3.price total_price "
                 "from flight F1, flight F2, flight F3, seat S1, "
                 "seat S2, seat S3 "
                 "where F1.code = S1.code and "
                 "F1.flight_no = S1.flight_no and "
                 "F1.time_depart = S1.time_depart and "
                 "F2.code = S2.code and "
                 "F2.flight_no = S2.flight_no and "
                 "F2.time_depart = S2.time_depart and "
                 "F3.code = S3.code and "
                 "F3.flight_no = S3.flight_no and "
                 "F3.time_depart = S3.time_depart and "
                 "date(F1.time_depart) = :date and "
                 "F1.airport_depart = :airport_depart and "
                 "F1.airport_arrival = F2.airport_depart and "
                 "F2.airport_arrival = F3.airport_depart and "
                 "F3.airport_arrival = :airport_arrival and "
                 "F2.time_depart > F1.time_arrival + interval "
                 "\'30 minutes\' and "
                 "F2.time_depart < F1.time_arrival + interval "
                 "\'1 day\' and "
                 "F3.time_depart > F2.time_arrival + interval "
                 "\'30 minutes\' and "
                 "F3.time_depart < F2.time_arrival + interval "
                 "\'1 day\' and "
                 "S1.current < S1.max and "
                 "S2.current < S2.max and "
                 "S3.current < S3.max"))
    keys = {'date': date, 'airport_depart': airport_depart,
                        'airport_arrival': airport_arrival}
    if max_stops == 0:
        with engine.connect() as conn:
                result = conn.execute(sql0, keys)
                conn.close()
        flights = []
        for row in result:
            flights.append(row[0:])
        if not flights:
            print('No flights found with the given criteria.')
            return False
        else:
            print('Success!')
            return flights
    elif max_stops == 1:
        with engine.connect() as conn:
                result = conn.execute(sql0, keys)
                conn.close()
        flights0 = []
        for row in result:
            flights0.append(row[0:])
        with engine.connect() as conn:
                result = conn.execute(sql1, keys)
                conn.close()
        flights1 = []
        for row in result:
            flights1.append(row[0:])
        if not flights0 and not flights1:
            print('No flights found with the given criteria.')
            return False
        else:
            print('Success!')
            return flights0, flights1
    elif max_stops == 2:
        with engine.connect() as conn:
                result = conn.execute(sql0, keys)
                conn.close()
        flights0 = []
        for row in result:
            flights0.append(row[0:])
        with engine.connect() as conn:
                result = conn.execute(sql1, keys)
                conn.close()
        flights1 = []
        for row in result:
            flights1.append(row[0:])
        with engine.connect() as conn:
                result = conn.execute(sql2, keys)
                conn.close()
        flights2 = []
        for row in result:
            flights2.append(row[0:])
        if not flights0 and not flights1 and not flights2:
            print('No flights found with the given criteria.')
            return False
        else:
            print('Success!')
            return flights0, flights1, flights2
    else:
        print('Up to two stops are permitted in an itinerary.')
        return False


"""
prior to create_booking, we get next booking_id
"""
def get_booking_id():

    """
    obtaining the current max booking_id
    If booking_id == None then booking_id = 11111111
    else booking_id = booking_id +1
    """

    sql = text(("select case when count(*) = 0 then \'0\' else max(booking_id) end from booking"))

    with engine.connect() as conn:
        result = conn.execute(sql)
        conn.close()

    resultSet = []

    for row in result:
        resultSet.append(row[0:])

    booking_id = resultSet[0][0]

    if booking_id == None:
        booking_id = 11111111
    else:
        booking_id = str(int(booking_id) + 1);

    return booking_id

"""
insert each flight segment as a separate row with the same booking_id
"""
def create_booking(booking_id, email, code, flight_no, time_depart, first_name, last_name, type, billing_id):

    sql = text(("insert into booking values(:booking_id, :email, :code, :flight_no, :time_depart, :first_name, :last_name, :type, :billing_id)"))
    keys = {'booking_id':booking_id, 'email': email, 'code':code, 'flight_no':flight_no, 'time_depart':time_depart, 'first_name':first_name, 'last_name':last_name,   'type':type, 'billing_id':billing_id}

    try:
        with engine.connect() as conn:
            conn.execute(sql, keys)
        conn.close()
        print('Booking created!')

        """
        update miles for booking
        """
        calculate_miles(booking_id)

        """
        increment current seat by 1
        """

        print ('Booking seat type: ' + type)

        sql=text(('update seat set current = current + 1 where code = :code and flight_no = :flight_no and time_depart = :time_depart and type = :type'))
        keys = {'code':code, 'flight_no':flight_no, 'time_depart':time_depart, 'type': type}

        try:
            with engine.connect() as conn:
                conn.execute(sql, keys)
            conn.close()
            print('Number of seats updated!')
        except:
            print('Issue updating seats.')
            conn.close()

    except:
        print('Issue creating booking.')
        conn.close()



# delete booking
# remove bonus miles
# sub 1 from the current seat
def cancel_booking(booking_id):

    try:
        """
        remove bonus miles
        """
        remove_miles(booking_id)

        """
        substract 1 from current seat
        To do that we need to obtain:
        code, flight_no, time_depart, type from booking
        """

        #obtain parameters of booking by booking_id
        sql=text(('select code, flight_no, time_depart, type from booking where booking_id=:booking_id'))
        keys = {'booking_id': str(booking_id)}

        with engine.connect() as conn:
            result = conn.execute(sql, keys)
            conn.close()

        bookingSegments = []
        for row in result:
            bookingSegments.append(row[0:])

        #iterate over flight segments and decrement number of seats occupied
        for segment in bookingSegments:

            code = segment[0]
            flight_no = segment[1]
            time_depart = segment[2]
            type = segment[3]


            print ('Booking seat type: ' + type)

            sql=text(('update seat set current = current - 1 where code = :code and flight_no = :flight_no and time_depart = :time_depart and type = :type'))
            keys = {'code':code, 'flight_no':flight_no, 'time_depart':time_depart, 'type': type}

            try:
                with engine.connect() as conn:
                    conn.execute(sql, keys)
                    conn.close()
                    print('Number of seats updated!')
            except:
                print('Issue updating seats.')
                conn.close()

        """
        delete booking
        """
        sql = text(("delete from booking where booking_id=:booking_id"))
        keys = {'booking_id': str(booking_id)}

        try:
            with engine.connect() as conn:
                conn.execute(sql, keys)
            conn.close()
            print('Booking canceled!')
        except:
            print('Booking was NOT cancelled.')
            conn.close()

    except:
        print('Issue canceling the booking.')
        conn.close()

# calculate miles by summing distance for each segment from 'flight' relation (distance for each record with the same booking number)
# and inserting the result for the booking owner
def calculate_miles(booking_id):

    """
    first, calculating bonus miles for the flights (booking)
    """
    sql = text(("select booking_id, email, code, distance, type from booking inner join flight using(code, flight_no, time_depart) "
                "where booking_id=:booking_id"))
    keys = {'booking_id': str(booking_id)}

    with engine.connect() as conn:
        result = conn.execute(sql, keys)
        conn.close()

    bookingSegments = []
    for row in result:
        bookingSegments.append(row[0:])

    """
    insert/update miles in mileage_program for the booking owner
    """

    for segment in bookingSegments:
        """"
        check whether mileage_program exists for the bookingOwner
        if True - update miles
        else - insert miles
        """

        bookingOwner = segment[1]
        airline = segment[2]
        type = segment[4]

        #for first class seat - number of bonus miles = distance *3
        #for business - number of bonus miles = distance *2
        if type == 'economy':
            miles = segment[3]
        elif type == 'first':
            miles = segment[3]*3
        elif type == 'business':
            miles = segment[3]*2

        sql = text(('select count(*) from mileage_program where email = :bookingOwner and code = :airline'))
        keys = {'bookingOwner': bookingOwner, 'airline': airline}

        with engine.connect() as conn:
            result = conn.execute(sql, keys)
            conn.close()

        resultSet = []
        for row in result:
            resultSet.append(row[0:])

        if resultSet[0][0] == 0:
            print('User is not part of mileage program')
            #insert user miles
            sql = text(('insert into mileage_program values(:email, :code, :bonus_miles)'))
            keys = {'email': bookingOwner, 'code': airline, 'bonus_miles': miles}
            try:
                with engine.connect() as conn:
                    conn.execute(sql, keys)
                conn.close()
                print('Success!')
            except:
                print('Issue committing to database.')
                conn.close()
        else:
            print('User is a part of mileage_program!')
            #update user miles
            sql = text(('update mileage_program set bonus_miles = bonus_miles + :add_miles where email = :email and code=:code'))
            keys = {'email': bookingOwner, 'code': airline, 'add_miles': miles}
            try:
                with engine.connect() as conn:
                    conn.execute(sql, keys)
                conn.close()
                print('Update succefull!')
            except:
                print('Issue committing to database.')
                conn.close()


# remove miles calculates number of miles to be removed
# for each flight segment and airline of booking to be deleted
def remove_miles(booking_id):

    """
    first, calculating bonus miles for the flights (booking)
    """
    sql = text(("select booking_id, email, code, distance, type from booking inner join flight using(code, flight_no, time_depart) "
                "where booking_id=:booking_id"))
    keys = {'booking_id': str(booking_id)}

    with engine.connect() as conn:
        result = conn.execute(sql, keys)
        conn.close()

    bookingSegments = []
    for row in result:
        bookingSegments.append(row[0:])

    """
    update (substract) miles in mileage_program for the booking owner
    """

    for segment in bookingSegments:
        """"
        check whether mileage_program exists for the bookingOwner
        if True - update miles (substract)
        else - print ('User is not a part of mileage_program')
        """

        bookingOwner = segment[1]
        airline = segment[2]
        type = segment[4]

        #for first class seat - number of bonus miles = distance *3
        #for business - number of bonus miles = distance *2
        if type == 'economy':
            miles = segment[3]
        elif type == 'first':
            miles = segment[3]*3
        elif type == 'business':
            miles = segment[3]*2

        sql = text(('select count(*) from mileage_program where email = :bookingOwner and code = :airline'))
        keys = {'bookingOwner': bookingOwner, 'airline': airline}

        with engine.connect() as conn:
            result = conn.execute(sql, keys)
            conn.close()

        resultSet = []
        for row in result:
            resultSet.append(row[0:])

        if resultSet[0][0] == 0:
            print('User is not part of mileage program')
        else:
            print('User is a part of mileage_program!')
            #update user miles
            sql = text(('update mileage_program set bonus_miles = bonus_miles - :add_miles where email = :email and code=:code'))
            keys = {'email': bookingOwner, 'code': airline, 'add_miles': miles}
            try:
                with engine.connect() as conn:
                    conn.execute(sql, keys)
                conn.close()
                print('Update succefull!')
            except:
                print('Issue committing to database.')
                conn.close()
