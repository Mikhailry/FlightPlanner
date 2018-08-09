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

class NewPaymentApp(server.App):
    title = 'New Payment'

    inputs = [{
        "type": "text",
        "key": "id",
        "label": "id",
        "action_id": "create_payment"
        },
        {
        "type": "text",
        "key": "name",
        "label": "name",
        "action_id": "create_payment"
        },
        {
        "type": "text",
        "key": "card_no",
        "label": "card number",
        "action_id": "create_payment"
        },
        {
        "type": "text",
        "key": "exp_mo",
        "label": "exp month",
        "action_id": "create_payment"
        },
        {
        "type": "text",
        "key": "exp_yr",
        "label": "exp year",
        "action_id": "create_payment"
        },
        {
        "type": "text",
        "key": "a_id",
        "label": "address id",
        "action_id": "create_payment"
    }]

    controls = [
        {
        "type": "button",
        "id": "create_payment",
        "label": "Edit",
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
        "id": "create_payment",
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

    def create_payment(self, params):
        if 'user' in cherrypy.session:
            errors = []
            b_id = params['id']
            name = params['name']
            card_no = params['card_no']
            exp_mo = params['exp_mo']
            exp_yr = params['exp_yr']
            a_id = params['a_id']
            if not b_id:
                errors.append('Billing ID field is empty')
            if not name:
                errors.append('Name field is empty')
            if not card_no:
                errors.append('Card Number field is empty')
            if not exp_mo:
                errors.append('Exp Month field is empty')
            if not exp_yr:
                errors.append('Exp Year field is empty')
            if not a_id:
                errors.append('Adress ID field is empty')
            if b_id and name and card_no and exp_mo and exp_yr and a_id:
                success = project.add_payment(cherrypy.session['user'][0], b_id, name, card_no, exp_mo, exp_yr, a_id)
                if success:
                    return "<b>Success</b>"
                else:
                    return "There was an error processing your request. Please contact an administrator"
            else:
                return env.get_template('login.html').render(errors=errors)
        else:
            return "<b>You are not logged in</b>"


class EditPaymentApp(server.App):
    title = 'Edit Payment'

    inputs = [{
        "type": "text",
        "key": "id",
        "label": "id",
        "action_id": "edit_payment"
        },
        {
        "type": "text",
        "key": "name",
        "label": "name",
        "action_id": "edit_payment"
        },
        {
        "type": "text",
        "key": "card_no",
        "label": "card number",
        "action_id": "edit_payment"
        },
        {
        "type": "text",
        "key": "exp_mo",
        "label": "exp month",
        "action_id": "edit_payment"
        },
        {
        "type": "text",
        "key": "exp_yr",
        "label": "exp year",
        "action_id": "edit_payment"
        },
        {
        "type": "text",
        "key": "a_id",
        "label": "address id",
        "action_id": "edit_payment"
    }]

    controls = [
        {
        "type": "button",
        "id": "edit_payment",
        "label": "Edit",
        },
        {
        "type": "button",
        "id": "search_data",
        "label": "Refresh Data"
        }
    ]

    outputs = [{
        "type": "table",
        "id": "search_billing",
        "control_id": "search_data",
        "tab": "Payments",
        "on_page_load": True
        },
        {
        "type": "table",
        "id": "search_address",
        "control_id": "search_data",
        "tab": "Addresses",
        "on_page_load": True
        },
        {
        "type": "html",
        "id": "edit_payment",
        "on_page_load": False
        }
    ]

    tabs = ["Payments", "Addresses"]

    def search_billing(self, params):
        empty = [[]]
        for _ in range(9):
            empty[0].append("")
        result = empty
        if "session" in dir(cherrypy):
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
                result = project.get_payments(email)
                if not result:
                    result = empty
        return pd.DataFrame(np.array(result),
            columns = ["Email", "Billing ID",
            "Name", "Card Number",
            "Exp Month", "Exp Year", "Address ID"])

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

    def edit_payment(self, params):
        if 'user' in cherrypy.session:
            errors = []
            b_id = params['id']
            name = params['name']
            card_no = params['card_no']
            exp_mo = params['exp_mo']
            exp_yr = params['exp_yr']
            a_id = params['a_id']
            if not b_id:
                errors.append('Billing ID field is empty')
            if not name:
                errors.append('Name field is empty')
            if not card_no:
                errors.append('Card Number field is empty')
            if not exp_mo:
                errors.append('Exp Month field is empty')
            if not exp_yr:
                errors.append('Exp Year field is empty')
            if not a_id:
                errors.append('Adress ID field is empty')
            if b_id and name and card_no and exp_mo and exp_yr and a_id:
                success = project.edit_payment(cherrypy.session['user'][0], b_id, name, card_no, exp_mo, exp_yr, a_id)
                if success:
                    return "<b>Success</b>"
                else:
                    return "There was an error processing your request. Please contact an administrator"
            else:
                return env.get_template('login.html').render(errors=errors)
        else:
            return "<b>You are not logged in</b>"

class DeletePaymentApp(server.App):
    title = 'Delete Payment'

    inputs = [{
        "type": "text",
        "key": "id",
        "label": "id",
        "action_id": "delete_payment"
        }
    ]

    controls = [
        {
        "type": "button",
        "id": "delete_payment",
        "label": "Delete",
        },
        {
        "type": "button",
        "id": "search_data",
        "label": "Refresh Data"
        }
    ]

    outputs = [{
        "type": "table",
        "id": "search_billing",
        "control_id": "search_data",
        "on_page_load": True
        },
        {
        "type": "html",
        "id": "delete_payment",
        "on_page_load": False
        }
    ]

    def search_billing(self, params):
        empty = [[]]
        for _ in range(9):
            empty[0].append("")
        result = empty
        if "session" in dir(cherrypy):
            if "user" in cherrypy.session:
                email = cherrypy.session["user"][0]
                result = project.get_payments(email)
                if not result:
                    result = empty
        return pd.DataFrame(np.array(result),
            columns = ["Email", "Billing ID",
            "Name", "Card Number",
            "Exp Month", "Exp Year", "Address ID"])

    def delete_payment(self, params):
        if 'user' in cherrypy.session:
            errors = []
            p_id = params['id']
            if not p_id:
                errors.append("You must enter a Billing ID")
                return env.get_template('login.html').render(errors=errors)
            else:
                success = project.delete_payment(cherrypy.session['user'][0], p_id)
                if success:
                    return "<b>Success</b>"
                else:
                    return "There was an error processing your request. Please contact an administrator"
        else:
            return "<b>You are not logged in</b>"