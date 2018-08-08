from spyre import server
import project
import jinja2
import pandas as pd
import numpy as np
import cherrypy
import datetime
import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=ROOT_DIR)
env = jinja2.Environment(loader=templateLoader)

class FindFlightsApp(server.App):
    title = "Find Flights"
    inputs = [{
        "type": "dropdown",
        "key": "airport_depart",
        "label": "Departure Airport",
        "options": list(map(lambda x: {"value": x[0],
            "label": x[0] + ": " + x[1]},project.get_airports()))
        },
        {
        "type": "dropdown",
        "key": "airport_arrival",
        "label": "Destination Airport",
        "options": list(map(lambda x: {"value": x[0],
            "label": x[0] + ": " + x[1]},project.get_airports()))
        },
        {
        "type": "text",
        "key": "date",
        "label": "Departure Date",
        "value": "YYYY-MM-DD"
        },
        {
        "type": "dropdown",
        "key": "stops",
        "label": "Number of Stops",
        "options": [{"label": "0", "value": "0"},
            {"label": "1", "value": "1"},
            {"label": "2", "value": "2"}]
        }
    ]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Search"
    }]

    outputs = [{
        "type": "table",
        "id": "find_flights",
        "control_id": "update_data",
        "on_page_load": True
        },
        {"type": "html",
        "id": "errors",
        "control_id": "update_data",
        "on_page_load": False
        },
    ]

    def invalid_date(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return False
        except:
            return "Incorrect entry format in Departure Date field."

    def errors(self, params):
        if "session" not in dir(cherrypy):
            return
        else:
            if "errors" not in cherrypy.session:
                return
            else:
                errors = cherrypy.session["errors"]
                error_str = "<h2>Errors:</h2>" + "<br>" + "<ul>"
                for x in errors:
                    error_str = error_str + "<li>" + x + "</li>"
                error_str = error_str + "</ul>"
                del cherrypy.session["errors"]
                return error_str

    def find_flights(self, params):
        errors = []
        empty = [[]]
        for _ in range(8):
            empty[0].append("")
        result = pd.DataFrame(np.array(empty),
            columns = ["Airline", "Code", "Departure Airport",
                       "Arrival Airport", "Departure Time",
                       "Arrival Time", "Class", "Price"])
        airport_depart = params["airport_depart"]
        airport_arrival = params["airport_arrival"]
        date = params["date"]
        stops = params["stops"]

        if "errors" in cherrypy.session:
            del cherrypy.session["errors"]
        if not airport_depart:
            errors.append("Departure Airport field is empty.")
        if not airport_arrival:
            errors.append("Destination Airport field is empty.")
        if not date:
            errors.append("Departure Date field is empty.")
        elif self.invalid_date(date):
            errors.append(self.invalid_date(date))
            date = ""
        if airport_depart and airport_arrival and date:
            flights = project.find_flights(date, airport_depart,
                airport_arrival, 2)
            if flights:
                if stops == "0" and flights[0]:    
                    result = pd.DataFrame(np.array(flights[0]),
                        columns = ["Airline", "Code",
                        "Departure Airport", "Arrival Airport",
                        "Departure Time", "Arrival Time", "Class",
                        "Price"])
                elif stops == "1" and flights[1]:
                    result = pd.DataFrame(np.array(flights[1]),
                        columns = ["Flight 1: Airline",
                        "Flight 1: Code",
                        "Flight 1: Departure Airport",
                        "Flight 1: Arrival Airport",
                        "Flight 1: Departure Time",
                        "Flight 1: Arrival Time", "Flight 2: Airline",
                        "Flight 2: Code", "Flight 2: Departure Airport",
                        "Flight 2: Arrival Airport",
                        "Flight 2: Departure Time",
                        "Flight 2: Arrival Time", "Flight 1: Class",
                        "Flight 2: Class", "Total Price"])
                elif stops == "2" and flights[2]:
                    result = pd.DataFrame(np.array(flights[2]),
                        columns = ["Flight 1: Airline",
                        "Flight 1: Code",
                        "Flight 1: Departure Airport",
                        "Flight 1: Arrival Airport",
                        "Flight 1: Departure Time",
                        "Flight 1: Arrival Time",
                        "Flight 2: Airline", "Flight 2: Code",
                        "Flight 2: Departure Airport",
                        "Flight 2: Arrival Airport",
                        "Flight 2: Departure Time",
                        "Flight 2: Arrival Time", "Flight 3: Airline",
                        "Flight 3: Code", "Flight 3: Departure Airport",
                        "Flight 3: Arrival Airport",
                        "Flight 3: Departure Time",
                        "Flight 3: Arrival Time", "Flight 1: Class",
                        "Flight 2: Class", "Flight 3: Class",
                        "Total Price"])
        if errors:
            cherrypy.session["errors"] = errors
        return result

class NewBookingApp(server.App):
    title = "New Booking"
    inputs = [{
        "type": "dropdown",
        "key": "code",
        "label": "Airline Code",
        "options": list(map(lambda x: {"value": x[0],
            "label": x[0] + ": " + x[1]}, project.get_airlines()))
        },
        {
        "type": "text",
        "key": "flight_no",
        "label": "Flight Number",
        "value": "0000"
        },
        {
        "type": "text",
        "key": "time_depart",
        "label": "Departure Timestamp",
        "value": "YYYY-MM-DD HH:MM:SS"
        },
        {
        "type": "text",
        "key": "first_name",
        "label": "Passenger First Name"
        },
        {
        "type": "text",
        "key": "last_name",
        "label": "Passenger Last Name"
        },
        {
        "type": "text",
        "key": "seat_type",
        "label": "Class"
        },
        {
        "type": "text",
        "key": "billing_id",
        "label": "Payment Method"
        }
    ]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Add to Booking"
        },
        {
        "type": "button",
        "id": "clear_data",
        "label": "Clear Booking"
        },
        {
        "type": "button",
        "id": "commit_data",
        "label": "Submit Booking"
    }]

    outputs = [{
        "type": "table",
        "id": "add_book",
        "control_id": "update_data",
        "on_page_load": False
        },
        {"type": "html",
        "id": "add_book_errors",
        "control_id": "update_data",
        "on_page_load": False
        },
        {
        "type": "html",
        "id": "clear_book",
        "control_id": "clear_data",
        "on_page_load": False
        },
        {
        "type": "html",
        "id": "commit_book",
        "control_id": "commit_data",
        "on_page_load": False
        }
    ]

    def invalid_time(self, time):
        try:
            datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        except:
            return "Incorrect entry format in Departure Timestamp field."

    def clear_book(self, params):
        if "session" in dir(cherrypy):
            if "booking" in cherrypy.session:
                cherrypy.session["booking"] = []
            if "billing_id" in cherrypy.session:
                del cherrypy.session["billing_id"]
        return "<h2>Booking cleared!</h2>"

    def commit_book(self, params):
        if "session" in dir(cherrypy):
            if "booking" not in cherrypy.session or not cherrypy.session["booking"]:
                return "<h2>New booking is empty.</h2>"
        msg = "<h2>Results:</h2><br><ul>"
        for x in cherrypy.session["booking"]:
            msg = msg + "<li>" + project.create_booking(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]) + "</li>"
        msg = msg + "</ul>"
        project.calculate_miles(cherrypy.session["booking_id"])
        del cherrypy.session["booking_id"]
        del cherrypy.session["billing_id"]
        del cherrypy.session["booking"]
        return msg

    def add_book(self, params):
        errors = []
        empty = [[]]
        for _ in range(9):
            empty[0].append("")
        if "session" not in dir(cherrypy):
            booking = []
            booking_id = ""
            billing_id = ""
            email = ""
        else:
            if "errors" in cherrypy.session:
                del cherrypy.session["errors"]
            if "booking" in cherrypy.session:
                booking = cherrypy.session["booking"]
            else:
                booking = []
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
            else:
                email = ""
            if "booking_id" in cherrypy.session:
                booking_id = cherrypy.session["booking_id"]
            else:
                cherrypy.session["booking_id"] = booking_id = project.get_booking_id()
            if "billing_id" in cherrypy.session:
                billing_id = cherrypy.session["billing_id"]
            else:
                if params["billing_id"]:
                    cherrypy.session["billing_id"] = billing_id = params["billing_id"]
                else:
                    billing_id = ""

        code = params["code"]
        flight_no = params["flight_no"]
        time_depart = params["time_depart"]
        first_name = params["first_name"]
        last_name = params["last_name"]
        seat_type = params["seat_type"]

        if not email:
            errors.append("User not logged in.")
        if not code:
            errors.append("Airline Code field is empty.")
        if not flight_no:
            errors.append("Flight Number field is empty.")
        if not time_depart:
            errors.append("Departure Timestamp field is empty.")
        if self.invalid_time(time_depart):
            errors.append(self.invalid_time(time_depart))
            time_depart = ""
        if not first_name:
            errors.append("First Name field is empty.")
        if not last_name:
            errors.append("Last Name field is empty.")
        if not seat_type:
            errors.append("Class field is empty.")
        if not billing_id:
            errors.append("Payment Method field is empty.")
        if email and code and flight_no and time_depart and first_name \
        and last_name and seat_type and billing_id:
            flight_new = (booking_id, email, code, flight_no, time_depart, first_name, last_name, seat_type, billing_id)
            exists = False
            for x in booking:
                if flight_new[2:7] == x[2:7]:
                    errors.append("A passenger with that name is already included in the booking for this flight.")
                    exists = True
            if exists == False:
                booking.append(flight_new)
                cherrypy.session["booking"] = booking
        if errors:
            cherrypy.session["errors"] = errors
        if not booking:
            booking = empty
        return pd.DataFrame(np.array(booking),
            columns = ["Booking ID", "Email", "Airline Code", "Flight Number",
            "Departure Timestamp", "First Name", "Last Name",
            "Class", "Payment Method"])

    def add_book_errors(self, params):
        if "session" not in dir(cherrypy):
            return
        else:
            if "errors" not in cherrypy.session:
                return
            else:
                errors = cherrypy.session["errors"]
                error_str = "<h2>Errors:</h2>" + "<br>" + "<ul>"
                for x in errors:
                    error_str = error_str + "<li>" + x + "</li>"
                error_str = error_str + "</ul>"
                del cherrypy.session["errors"]
                return error_str


class CancelBookingApp(server.App):
    title = 'Cancel Booking'
    inputs = [{
        "type": "text",
        "key": "booking_id",
        "label": "Booking ID",
        "value": "",
        "action_id": "update_data"
    }]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Cancel Booking"
        },
        {
        "type": "button",
        "id": "search_data",
        "label": "Refresh Current Bookings"
    }]

    outputs = [{
        "type": "table",
        "id": "search_book",
        "control_id": "search_data",
        "on_page_load": True
        },
        {
        "type": "html",
        "id": "cancel_book",
        "control_id": "update_data",
        "on_page_load": False
        }
    ]

    def search_book(self, params):
        empty = [[]]
        for _ in range(9):
            empty[0].append("")
        result = empty
        if "session" in dir(cherrypy):
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
                result = project.get_booking(email)
                if not result:
                    result = empty
        return pd.DataFrame(np.array(result),
            columns = ["Booking ID", "Email", "Airline Code",
            "Flight Number", "Departure Timestamp", "First Name",
            "Last Name", "Class", "Payment Method"])
        
    def cancel_book(self, params):
        errors = []
        if "session" not in dir(cherrypy):
            email = ""
        else:
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
            else:
                errors.append("User not logged in.")
        if not params["booking_id"]:
            errors.append("Booking ID field is empty.")
        else:
            booking_id = params["booking_id"]
        
        if errors:
            error_str = "<h2>Errors:</h2>" + "<br>" + "<ul>"
            for x in errors:
                error_str = error_str + "<li>" + x + "</li>"
            error_str = error_str + "</ul>"
            return error_str
        else:
            msg = project.cancel_booking(booking_id)
            return "<h2>" + msg + "</h2>"
