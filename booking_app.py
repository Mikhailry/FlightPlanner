from spyre import server
import jinja2
import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=ROOT_DIR)
env = jinja2.Environment(loader=templateLoader)

class NewBookingApp(server.App):
    title = 'New Booking'
    inputs = [{
        "type": "text",
        "key": "email",
        "label": "email",
        "action_id": "simple_html_output"
        },
        {
        "type": "text",
        "key": "password",
        "label": "password",
        "action_id": "simple_html_output"
        }
    ]

    outputs = [{
        "type": "html",
        "id": "simple_html_output"
    }]

    def getHTML(self, params):
        return ''

class CancelBookingApp(server.App):
    title = 'Cancel Booking'
    inputs = [{
        "type": "text",
        "key": "email",
        "label": "email",
        "action_id": "simple_html_output"
        },
        {
        "type": "text",
        "key": "password",
        "label": "password",
        "action_id": "simple_html_output"
        }
    ]

    outputs = [{
        "type": "html",
        "id": "simple_html_output"
    }]

    def getHTML(self, params):
        return ''