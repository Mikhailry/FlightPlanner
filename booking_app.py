from spyre import server
import project
import jinja2
import pandas as pd
import numpy as np
import cherrypy
from cherrypy.lib import sessions
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
        "options": list(map(lambda x: {"value": x[0], "label": x[0] + ": " + x[1]},project.get_airports())),
        "action_id": "update_data"
        },
        {
        "type": "dropdown",
        "key": "airport_arrival",
        "label": "Destination Airport",
        "options": list(map(lambda x: {"value": x[0], "label": x[0] + ": " + x[1]},project.get_airports())),
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "date",
        "label": "Departure Date",
        "value": "YYYY-MM-DD",
        "action_id": "update_data"
        },
        {
        "type": "dropdown",
        "key": "stops",
        "label": "Number of Stops",
        "options": [{"label": "0", "value": "0"},
            {"label": "1", "value": "1"},
            {"label": "2", "value": "2"}],
        "action_id": "update_data"
        }
    ]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Search"
    }]

    outputs = [{
        "type": "table",
        "id": "flights",
        "control_id": "update_data",
        "on_page_load": False
        }
    ]

    def getData(self, params):
        errors = []
        airport_depart = params["airport_depart"]
        airport_arrival = params["airport_arrival"]
        date = params["date"]
        stops = params["stops"]

        if not airport_depart:
            errors.append('Departure Airport field is empty')
        if not airport_arrival:
            errors.append('Destination Airport field is empty')
        if not date:
            errors.append('Departure Date field is empty')
        else:
            result = project.find_flights(date, airport_depart,
                airport_arrival, 2)
            if not result:
                return pd.DataFrame([])
            if stops == "0":    
                if not result[0]:
                    result_0 = pd.DataFrame([])
                else:
                    result_0 = pd.DataFrame(np.array(result[0]),
                    columns = ["Airline", "Code", "Departure Airport",
                    "Arrival Airport", "Departure Time", "Arrival Time",
                    "Class", "Price"])
                return result_0
            elif stops == "1":
                if not result[1]:
                    result_1 = pd.DataFrame([])
                else:
                    result_1 = pd.DataFrame(np.array(result[1]),
                    columns = ["Flight 1: Airline", "Flight 1: Code",
                    "Flight 1: Departure Airport",
                    "Flight 1: Arrival Airport",
                    "Flight 1: Departure Time",
                    "Flight 1: Arrival Time", "Flight 2: Airline",
                    "Flight 2: Code", "Flight 2: Departure Airport",
                    "Flight 2: Arrival Airport",
                    "Flight 2: Departure Time",
                    "Flight 2: Arrival Time", "Flight 1: Class",
                    "Flight 2: Class", "Total Price"])
                return result_1
            elif stops == "2":
                if not result[2]:
                    result_2 = pd.DataFrame([])
                else:
                    result_2 = pd.DataFrame(np.array(result[2]),
                    columns = ["Flight 1: Airline", "Flight 1: Code",
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
                return result_2

class NewBookingApp(server.App):
    title = "New Booking"
    inputs = [{
        "type": "text",
        "key": "code",
        "label": "Airline Code",
        "value": "AA",
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "flight_no",
        "label": "Flight Number",
        "value": "0000",
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "time_depart",
        "label": "Departure Timestamp",
        "value": "YYYY-MM-DD HH:MM:SS",
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "first_name",
        "label": "Passenger First Name",
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "last_name",
        "label": "Passenger Last Name",
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "seat_type",
        "label": "Class",
        "action_id": "update_data"
        },
        {
        "type": "text",
        "key": "billing_id",
        "label": "Payment Method",
        "action_id": "update_data"
        }
    ]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Add to Booking"
        },
        {
        "type": "button",
        "id": "clear_book",
        "label": "Clear Booking"
        },
        {
        "type": "button",
        "id": "commit_book",
        "label": "Submit Booking"
    }]

    outputs = [{
        "type": "table",
        "id": "add_book",
        "control_id": "update_data",
        "on_page_load": False
        },
        {
        "type": "html",
        "id": "clear_book",
        "control_id": "clear_book",
        "on_page_load": False
        },
        {
        "type": "html",
        "id": "commit_book",
        "control_id": "commit_book",
        "on_page_load": False
        }
    ]


    def clear_book(self, params):
        if "session" in dir(cherrypy):
            if "booking" in cherrypy.session:
                cherrypy.session["booking"] = []
        return "Clear Booking"

    def commit_book(self, params):
        if "session" in dir(cherrypy):
            if "booking" not in cherrypy.session or not cherrypy.session["booking"]:
                return "Submit Booking"
        else:
            return "Submit Booking"
        for x in cherrypy.session["booking"]:
            project.create_booking(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
        cherrypy.session["booking_id"] = ""
        cherrypy.session["billing_id"] = ""
        cherrypy.session["booking"] = []
        return "Submit Booking"

    def add_book(self, params):
        errors = []
        if "session" not in dir(cherrypy):
            booking = []
            booking_id = ""
            billing_id = ""
            email = ""
        else:
            if "booking" in cherrypy.session:
                booking = cherrypy.session["booking"]
            else:
                booking = []
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
            if "booking_id" in cherrypy.session:
                booking_id = cherrypy.session["booking_id"]
            else:
                cherrypy.session["booking_id"] = booking_id = project.get_booking_id()
            if "billing_id" in cherrypy.session:
                billing_id = cherrypy.session["billing_id"]
            else:
                cherrypy.session["billing_id"] = billing_id = params["billing_id"]

        code = params["code"]
        flight_no = params["flight_no"]
        time_depart = params["time_depart"]
        first_name = params["first_name"]
        last_name = params["last_name"]
        seat_type = params["seat_type"]

        if not email:
            errors.append('Not logged in')
        if not code:
            errors.append('Airline Code field is empty')
        if not flight_no:
            errors.append('Flight Number field is empty')
        if not time_depart:
            errors.append('Departure Timestamp field is empty')
        if not first_name:
            errors.append('First Name field is empty')
        if not last_name:
            errors.append('Last Name field is empty')
        if not seat_type:
            errors.append('Class field is empty')
        if not billing_id:
            errors.append('Payment Method field is empty')
        if email and code and flight_no and time_depart and first_name \
        and last_name and seat_type and billing_id:
            flight_new = (booking_id, email, code, flight_no, time_depart, first_name, last_name, seat_type, billing_id)
            if flight_new not in booking:
                booking.append(flight_new)
                cherrypy.session["booking"] = booking
            return pd.DataFrame(np.array(cherrypy.session["booking"]),
                columns = ["Booking ID", "Email", "Airline Code", "Flight Number",
                "Departure Timestamp", "First Name", "Last Name",
                "Class", "Payment Method"])


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
    }]

    outputs = [{
        "type": "html",
        "id": "cancel_book",
        "control_id": "update_data",
        "on_page_load": False
        }
    ]

    def cancel_book(self, params):
        errors = []
        if "session" not in dir(cherrypy):
            email = ""
        else:
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
        booking_id = params["booking_id"]
        
        if not email:
            errors.append('Not logged in')
        if not booking_id:
            errors.append('Booking ID field is empty')
        if email and booking_id:
            project.cancel_booking(booking_id)
            return "Success!"