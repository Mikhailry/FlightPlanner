import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

DB_CONN = json.loads(open('database_connection.json', 'r').read())
engine = create_engine('postgresql://%s:%s@%s:%s/%s' %  
                      (DB_CONN['username'], DB_CONN['password'],
                       DB_CONN['hostname'], str(DB_CONN['port']),
                       DB_CONN['database']))

def create_tables():
    """
    Creates all tables necessary for a flight booking application.

    :returns: True is operation was successful, False otherwise
    """
    sql = text(("create table airline ("
                "code varchar(2), "
                "name varchar(50) not null, "
                "country varchar(50) not null, "
                "primary key (code));"
                "\n"
                "create table airport ("
                "code varchar(3), "
                "name varchar(100) not null, "
                "country varchar(50) not null, "
                "state varchar(2), "
                "primary key (code));"
                "\n"
                "create table customer ("
                "email varchar(50), "
                "password varchar(50) not null, "
                "first_name varchar(50) not null, "
                "last_name varchar(50) not null, "
                "airport varchar(3) not null, "
                "primary key (email), "
                "foreign key (airport) references airport(code));"
                "\n"
                "create table customer_address ("
                "email varchar(50), "
                "address_id varchar(20), "
                "name varchar(50) not null, "
                "address_line_1 varchar(50) not null, "
                "address_line_2 varchar(50) not null, "
                "city varchar(50) not null, "
                "state varchar(2) not null, "
                "zip varchar(10) not null, "
                "phone_no varchar(15), "
                "primary key (email, address_id), "
                "foreign key (email) references customer);"
                "\n"
                "create table customer_billing ("
                "email varchar(50), "
                "billing_id varchar(20), "
                "name varchar(50) not null, "
                "card_no numeric(16, 0) not null, "
                "exp_mo varchar(2) not null, "
                "exp_hr int not null, "
                "address_id varchar(20), "
                "primary key (email, billing_id), "
                "foreign key (email, address_id) references "
                "customer_address on delete cascade);"
                "\n"
                "create table flight ("
                "code varchar(2), "
                "flight_no int, "
                "date date, airport_depart varchar(3) not null, "
                "airport_arrival varchar(3) not null, "
                "time_depart timestamp not null, "
                "time_arrival timestamp not null, "
                "seat_current_first int not null, "
                "seat_current_econ int not null, "
                "seat_max_first int not null, "
                "seat_max_econ int not null, "
                "price_first numeric(8, 2) not null, "
                "price_econ numeric(8, 2) not null, "
                "primary key (code, flight_no, date), "
                "foreign key (airport_depart) references "
                "airport(code), "
                "foreign key (airport_arrival) references "
                "airport(code), "
                "foreign key (code) references airline);"
                "\n"
                "create table booking ("
                "booking_id varchar(10), "
                "email varchar(50), "
                "code varchar(2), "
                "flight_no int, "
                "date date, "
                "first_name varchar(50), "
                "last_name varchar(50), "
                "class varchar(5) not null, "
                "billing_id varchar(20), "
                "primary key (booking_id, email, code, flight_no, "
                "date, first_name, last_name), "
                "foreign key (email, billing_id) references "
                "customer_billing, "
                "foreign key (code, flight_no, date) references "
                "flight);"
                "\n"
                "create table mileage_program ("
                "email varchar(50), "
                "code varchar(2), "
                "bonus_miles int not null default 0, "
                "primary key (email, code), "
                "foreign key (email) references customer, "
                "foreign key (code) references airline);"))
    try:
        with engine.connect() as conn:
            conn.execute(sql)
        print('Success!')
        return True
    except:
        print('Issue committing to database.')
        return False

def drop_tables():
    """
    Drops all flight application tables from the database.sql

    :returns: True if operation was successful, False otherwise
    """
    sql = text(("drop table mileage_program, booking, flight, "
                "customer_billing, customer_address, customer, "
                "airport, airline"))
    try:
        with engine.connect() as conn:
            conn.execute(sql)
        print('Success!')
        return True
    except:
        print('Issue committing to database.')
        return False

def load_sample_data():
    """
    Loads sample data into the application to enable quick validation
    of the API

    :returns: True if the operation was successful, False otherwise
    """
    sql = text(("insert into airline values "
                "(:al_1, :al_2, :al_3);"
                "\n"
                "insert into airport values "
                "(:ap_1_1, :ap_1_2, :ap_1_3, :ap_1_4), "
                "(:ap_2_1, :ap_2_2, :ap_2_3, :ap_2_4), "
                "(:ap_3_1, :ap_3_2, :ap_3_3, :ap_3_4), "
                "(:ap_4_1, :ap_4_2, :ap_4_3, :ap_4_4);"
                "\n"
                "insert into customer values "
                "(:c_1, :c_2, :c_3, :c_4, :c_5);"
                "\n"
                "insert into customer_address values "
                "(:ca_1_1, :ca_1_2, :ca_1_3, :ca_1_4, :ca_1_5, "
                ":ca_1_6, :ca_1_7, :ca_1_8, :ca_1_9), "
                "(:ca_2_1, :ca_2_2, :ca_2_3, :ca_2_4, :ca_2_5, "
                ":ca_2_6, :ca_2_7, :ca_2_8, :ca_2_9);"
                "\n"
                "insert into customer_billing values "
                "(:cb_1_1, :cb_1_2, :cb_1_3, :cb_1_4, :cb_1_5, "
                ":cb_1_6, :cb_1_7), "
                "(:cb_2_1, :cb_2_2, :cb_2_3, :cb_2_4, :cb_2_5, "
                ":cb_2_6, :cb_2_7);"
                "\n"
                "insert into flight values "
                "(:f_1_1, :f_1_2, :f_1_3, :f_1_4, :f_1_5, :f_1_6, "
                ":f_1_7, :f_1_8, :f_1_9, :f_1_10, :f_1_11, :f_1_12, "
                ":f_1_13), "
                "(:f_2_1, :f_2_2, :f_2_3, :f_2_4, :f_2_5, :f_2_6, "
                ":f_2_7, :f_2_8, :f_2_9, :f_2_10, :f_2_11, :f_2_12, "
                ":f_2_13), "
                "(:f_3_1, :f_3_2, :f_3_3, :f_3_4, :f_3_5, :f_3_6, "
                ":f_3_7, :f_3_8, :f_3_9, :f_3_10, :f_3_11, :f_3_12, "
                ":f_3_13);"
                "\n"
                "insert into booking values "
                "(:b_1_1, :b_1_2, :b_1_3, :b_1_4, :b_1_5, :b_1_6, "
                ":b_1_7, :b_1_8, :b_1_9), "
                "(:b_2_1, :b_2_2, :b_2_3, :b_2_4, :b_2_5, :b_2_6, "
                ":b_2_7, :b_2_8, :b_2_9);"
                "\n"
                "insert into mileage_program values "
                "(:m_1, :m_2, :m_3);"))
    keys = {"al_1": "AA", "al_2": "American Airlines", "al_3": "USA",
            "ap_1_1": "ORD", "ap_1_2": "O\'hare", "ap_1_3": "USA",
            "ap_1_4": "IL", "ap_2_1": "LAX", "ap_2_2": "LA Int", 
            "ap_2_3": "USA", "ap_2_4": "CA", "ap_3_1": "IAD",
            "ap_3_2": "Dulles", "ap_3_3": "USA", "ap_3_4": "VA",
            "ap_4_1": "DCA", "ap_4_2": "Reagan", "ap_4_3": "USA",
            "ap_4_4": "DC", "c_1": "foo@bar.com", "c_2": "password",
            "c_3": "John", "c_4": "Doe", "c_5": "ORD",
            "ca_1_1": "foo@bar.com", "ca_1_2": "Home",
            "ca_1_3": "John Smith", "ca_1_4": "123 Cherry Ln.",
            "ca_1_5": "", "ca_1_6": "Chicago", "ca_1_7": "IL",
            "ca_1_8": "00000", "ca_1_9": "12345678901",
            "ca_2_1": "foo@bar.com", "ca_2_2": "Work",
            "ca_2_3": "John Smith", "ca_2_4": "321 Apple Rd.",
            "ca_2_5": "#123", "ca_2_6": "Chicago", "ca_2_7": "IL",
            "ca_2_8": "99999", "ca_2_9": "09876543210",
            "cb_1_1": "foo@bar.com", "cb_1_2": "Visa",
            "cb_1_3": "John Smith", "cb_1_4": "1234567887654321",
            "cb_1_5": "01", "cb_1_6": "01", "cb_1_7": "Home",
            "cb_2_1": "foo@bar.com", "cb_2_2": "Mastercard",
            "cb_2_3": "John Smith", "cb_2_4": "8765432112345678",
            "cb_2_5": "05", "cb_2_6": "05", "cb_2_7": "Work",
            "f_1_1": "AA", "f_1_2": "0001", "f_1_3": "2001-01-01",
            "f_1_4": "LAX", "f_1_5": "ORD", "f_1_6": "2001-01-01 09:00",
            "f_1_7": "2001-01-01 12:00", "f_1_8": 20, "f_1_9": 20,
            "f_1_10": 40, "f_1_11": 100, "f_1_12": 400,
            "f_1_13": 200, "f_2_1": "AA", "f_2_2": "0002",
            "f_2_3": "2001-01-01", "f_2_4": "ORD", "f_2_5": "IAD",
            "f_2_6": "2001-01-01 13:00", "f_2_7": "2001-01-01 15:00",
            "f_2_8": 1, "f_2_9": 20, "f_2_10": 0, "f_2_11": 100,
            "f_2_12": 200, "f_2_13": 100, "f_3_1": "AA",
            "f_3_2": "0003", "f_3_3": "2001-01-01", "f_3_4": "IAD",
            "f_3_5": "DCA", "f_3_6": "2001-01-01 16:00",
            "f_3_7": "2001-01-01 17:00", "f_3_8": 0, "f_3_9": 20,
            "f_3_10": 100, "f_3_11": 100, "f_3_12": 100,
            "f_3_13": 50, "b_1_1": 1, "b_1_2": "foo@bar.com",
            "b_1_3": "AA", "b_1_4": "0001", "b_1_5": "2001-01-01",
            "b_1_6": "John", "b_1_7": "Smith", "b_1_8": "first",
            "b_1_9": "Visa", "b_2_1": 1, "b_2_2": "foo@bar.com",
            "b_2_3": "AA", "b_2_4": "0001", "b_2_5": "2001-01-01",
            "b_2_6": "Jane", "b_2_7": "Doe", "b_2_8": "first",
            "b_2_9": "Visa", "m_1": "foo@bar.com", "m_2": "AA",
            "m_3": 800}
    try:
        with engine.connect() as conn:
            conn.execute(sql, keys)
        print('Success!')
        return True
    except:
        print('Issue committing to database.')
        return False