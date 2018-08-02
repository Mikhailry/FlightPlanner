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
                "flight_no varchar(4), "
                "time_depart timestamp not null, "
                "time_arrival timestamp not null, "
                "airport_depart varchar(3) not null, "
                "airport_arrival varchar(3) not null, "
                "distance int not null, "
                "primary key (code, flight_no, time_depart), "
                "foreign key (airport_depart) references "
                "airport(code), "
                "foreign key (airport_arrival) references "
                "airport(code), "
                "foreign key (code) references airline);"
                "\n"
                "create table seat ("
                "code varchar(2), "
                "flight_no varchar(4), "
                "time_depart timestamp, "
                "type varchar(25) not null, "
                "current int not null default 0, "
                "max int not null default 0, "
                "price numeric(8, 2) not null default 0, "
                "primary key (code, flight_no, time_depart, type), "
                "foreign key (code, flight_no, time_depart) references "
                "flight on update cascade, "
                "check (current <= max));"
                "\n"
                "create table booking ("
                "booking_id varchar(10), "
                "email varchar(50), "
                "code varchar(2), "
                "flight_no varchar(4), "
                "time_depart timestamp, "
                "first_name varchar(50) not null, "
                "last_name varchar(50) not null, "
                "type varchar(25) not null, "
                "billing_id varchar(20), "
                "primary key (booking_id, email, code, flight_no, "
                "time_depart), "
                "foreign key (email, billing_id) references "
                "customer_billing on delete set null, "
                "foreign key (code, flight_no, time_depart) references "
                "flight on update cascade, "
                "foreign key (code, flight_no, time_depart, type) "
                "references seat);"
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
    sql = text(("drop table mileage_program, booking, seat, flight, "
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
                ":f_1_7), "
                "(:f_2_1, :f_2_2, :f_2_3, :f_2_4, :f_2_5, :f_2_6, "
                ":f_2_7), "
                "(:f_3_1, :f_3_2, :f_3_3, :f_3_4, :f_3_5, :f_3_6, "
                ":f_3_7);"
                "\n"
                "insert into seat values "
                "(:s_1_1, :s_1_2, :s_1_3, :s_1_4, :s_1_5, :s_1_6, "
                ":s_1_7), "
                "(:s_2_1, :s_2_2, :s_2_3, :s_2_4, :s_2_5, :s_2_6, "
                ":s_2_7), "
                "(:s_3_1, :s_3_2, :s_3_3, :s_3_4, :s_3_5, :s_3_6, "
                ":s_3_7),"
                "(:s_4_1, :s_4_2, :s_4_3, :s_4_4, :s_4_5, :s_4_6, "
                ":s_4_7),"
                "(:s_5_1, :s_5_2, :s_5_3, :s_5_4, :s_5_5, :s_5_6, "
                ":s_5_7),"
                "(:s_6_1, :s_6_2, :s_6_3, :s_6_4, :s_6_5, :s_6_6, "
                ":s_6_7);"
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
            "f_1_1": "AA", "f_1_2": "0001", "f_1_3": "2001-01-01 09:00",
            "f_1_4": "2001-01-01 12:00", "f_1_5": "LAX", "f_1_6": "ORD",
            "f_1_7": 517, "f_2_1": "AA", "f_2_2": "0002",
            "f_2_3": "2001-01-01 13:00", "f_2_4": "2001-01-01 15:00",
            "f_2_5": "ORD", "f_2_6": "IAD", "f_2_7": 438, 
            "f_3_1": "AA", "f_3_2": "0003", "f_3_3": "2001-01-01 16:00",
            "f_3_4": "2001-01-01 17:00", "f_3_5": "IAD", "f_3_6": "DCA",
            "f_3_7": 319, "s_1_1": "AA", "s_1_2": "0001",
            "s_1_3": "2001-01-01 09:00", "s_1_4": "first", "s_1_5": 5,
            "s_1_6": 10, "s_1_7": 400, "s_2_1": "AA", "s_2_2": "0001",
            "s_2_3": "2001-01-01 09:00", "s_2_4": "business",
            "s_2_5": 10, "s_2_6": 20, "s_2_7": 300, "s_3_1": "AA",
            "s_3_2": "0001", "s_3_3": "2001-01-01 09:00",
            "s_3_4": "economy", "s_3_5": 50, "s_3_6": 80, "s_3_7": 150,
            "s_4_1": "AA", "s_4_2": "0002", "s_4_3": "2001-01-01 13:00",
            "s_4_4": "economy", "s_4_5": 10, "s_4_6": 20, "s_4_7": 300,
            "s_5_1": "AA", "s_5_2": "0003", "s_5_3": "2001-01-01 16:00",
            "s_5_4": "first", "s_5_5": 5, "s_5_6": 10, "s_5_7": 400,
            "s_6_1": "AA", "s_6_2": "0003", "s_6_3": "2001-01-01 16:00",
            "s_6_4": "economy", "s_6_5": 10, "s_6_6": 20, "s_6_7": 300,
            "b_1_1": 1, "b_1_2": "foo@bar.com",
            "b_1_3": "AA", "b_1_4": "0001", "b_1_5": "2001-01-01 09:00",
            "b_1_6": "John", "b_1_7": "Smith", "b_1_8": "business",
            "b_1_9": "Visa", "b_2_1": 1, "b_2_2": "foo@bar.com",
            "b_2_3": "AA", "b_2_4": "0002", "b_2_5": "2001-01-01 13:00",
            "b_2_6": "Jane", "b_2_7": "Doe", "b_2_8": "economy",
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

def frontend_query_placeholder(param):
    """
    Placeholder for any frontend queries.

    :returns: List if operation was successful, False otherwise
    """
    sql = text(("select stuff "
                "from table "
                "where column = :param"
                "order by stuff"))
    keys = {"thing": param}
    try:
        with engine.connect() as conn:
            conn.execute(sql, keys)
        resultSet = []
        for row in result:
            resultSet.append(row[0:])
        return resultSet
    except:
        print('Issue querying database.')
        return False