from spyre import server
import jinja2
import os
import project
import cherrypy
import pandas as pd
import numpy as np
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=ROOT_DIR)
env = jinja2.Environment(loader=templateLoader)

class NewAddressApp(server.App):
    title = 'New Address'

    inputs = [{
        "type": "text",
        "key": "id",
        "label": "id",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "name",
        "label": "name",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "line_1",
        "label": "line_1",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "line_2",
        "label": "line_2",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "city",
        "label": "city",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "state",
        "label": "state",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "zip",
        "label": "zip",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "phone",
        "label": "phone",
        "action_id": "create_address"
        }
    ]

    controls = [{
        "type": "button",
        "id": "create_address",
        "label": "Create"
    }]

    outputs = [{
        "type": "html",
        "id": "create_address",
        "on_page_load": False
        }
    ]

    def create_address(self, params):
        if 'user' in cherrypy.session:
            errors = []
            a_id = params['id']
            name = params['name']
            line_1 = params['line_1']
            line_2 = params['line_2']
            city = params['city']
            state = params['state']
            zipcode = params['zip']
            phone = params['phone']
            if not a_id:
                errors.append('Address ID field is empty')
            if not name:
                errors.append('Name field is empty')
            if not line_1:
                errors.append('Address Line 1 field is empty')
            if not city:
                errors.append('City field is empty')
            if not zipcode:
                errors.append('Zipcode field is empty')
            if not phone:
                errors.append('Phone field is empty')

            if a_id and name and line_1 and city and zipcode and phone:
                success = project.add_address(cherrypy.session['user'][0], a_id, name, line_1, line_2, city, state, zipcode, phone)
                if success:
                    return "<b>Success</b>"
                else:
                    return "There was an error processing your request. Please contact an administrator"
            else:
                return env.get_template('login.html').render(errors=errors)
        else:
            return "<b>You are not logged in</b>"

class EditAddressApp(server.App):
    title = 'Edit Address'

    inputs = [{
        "type": "text",
        "key": "id",
        "label": "id",
        "action_id": "create_address"
        },
        {
        "type": "text",
        "key": "name",
        "label": "name",
        "action_id": "edit_address"
        },
        {
        "type": "text",
        "key": "line_1",
        "label": "line_1",
        "action_id": "edit_address"
        },
        {
        "type": "text",
        "key": "line_2",
        "label": "line_2",
        "action_id": "edit_address"
        },
        {
        "type": "text",
        "key": "city",
        "label": "city",
        "action_id": "edit_address"
        },
        {
        "type": "text",
        "key": "state",
        "label": "state",
        "action_id": "edit_address"
        },
        {
        "type": "text",
        "key": "zip",
        "label": "zip",
        "action_id": "edit_address"
        },
        {
        "type": "text",
        "key": "phone",
        "label": "phone",
        "action_id": "edit_address"
        }
    ]

    controls = [
        {
        "type": "button",
        "id": "edit_address",
        "label": "Edit",
        },
        {
        "type": "button",
        "id": "search_data",
        "label": "Refresh Address List"
        }
    ]

    outputs = [{
        "type": "table",
        "id": "search_address",
        "control_id": "search_data",
        "on_page_load": True
        },
        {
        "type": "html",
        "id": "edit_address",
        "on_page_load": False
        }
    ]

    def search_address(self, params):
        empty = [[]]
        for _ in range(9):
            empty[0].append("")
        result = empty
        if "session" in dir(cherrypy):
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
                result = project.get_addresses(email)
                if not result:
                    result = empty
        return pd.DataFrame(np.array(result),
            columns = ["Email", "Address ID",
            "Name", "Address Line 1", "Address Line 2",
            "City", "State", "Zipcode", "Phone Number"])

    def edit_address(self, params):
        if 'user' in cherrypy.session:
            errors = []
            a_id = params['id']
            name = params['name']
            line_1 = params['line_1']
            line_2 = params['line_2']
            city = params['city']
            state = params['state']
            zipcode = params['zip']
            phone = params['phone']
            if not a_id:
                errors.append('Address ID field is empty')
            if not name:
                errors.append('Name field is empty')
            if not line_1:
                errors.append('Address Line 1 field is empty')
            if not city:
                errors.append('City field is empty')
            if not zipcode:
                errors.append('Zipcode field is empty')
            if not phone:
                errors.append('Phone field is empty')
            if a_id and name and line_1 and city and zipcode and phone:
                success = project.edit_address(cherrypy.session['user'][0], a_id, name, line_1, line_2, city, state, zipcode, phone)
                if success:
                    return "<b>Success</b>"
                else:
                    return "There was an error processing your request. Please contact an administrator"
            else:
                return env.get_template('login.html').render(errors=errors)
        else:
            return "<b>You are not logged in</b>"

class DeleteAddressApp(server.App):
    title = 'Delete Address'

    inputs = [{
        "type": "text",
        "key": "id",
        "label": "id",
        "action_id": "delete_address"
        }
    ]

    controls = [
        {
        "type": "button",
        "id": "delete_address",
        "label": "Delete",
        },
        {
        "type": "button",
        "id": "search_data",
        "label": "Refresh Address List"
        }
    ]

    outputs = [{
        "type": "table",
        "id": "search_address",
        "control_id": "search_data",
        "on_page_load": True
        },
        {
        "type": "html",
        "id": "delete_address",
        "on_page_load": False
        }
    ]

    def search_address(self, params):
        empty = [[]]
        for _ in range(9):
            empty[0].append("")
        result = empty
        if "session" in dir(cherrypy):
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
                result = project.get_addresses(email)
                if not result:
                    result = empty
        return pd.DataFrame(np.array(result),
            columns = ["Email", "Address ID",
            "Name", "Address Line 1", "Address Line 2",
            "City", "State", "Zipcode", "Phone Number"])

    def delete_address(self, params):
        if 'user' in cherrypy.session:
            errors = []
            a_id = params['id']
            if not a_id:
                errors.append("You must select an address ID")
                return env.get_template('login.html').render(errors=errors)
            else:
                success = project.delete_address(cherrypy.session['user'][0], a_id)
                if success:
                    return "<b>Success</b>"
                else:
                    return "There was an error processing your request. Please contact an administrator"
        else:
            return "<b>You are not logged in</b>"
