from spyre import server
import project
import jinja2
import os
import cherrypy
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=ROOT_DIR)
env = jinja2.Environment(loader=templateLoader)

class RegisterApp(server.App):
    title = 'Register'
    inputs = [{
        "type": "text",
        "key": "email",
        "label": "email",
        "action_id": "register"
        },
        {
        "type": "text",
        "key": "password",
        "label": "password",
        "action_id": "register"
        },
        {
        "type": "text",
        "key": "first",
        "label": "first name",
        "action_id": "register"
        },
        {
        "type": "text",
        "key": "last",
        "label": "last name",
        "action_id": "register"
        },
        {
        "type": "dropdown",
        "key": "airport",
        "label": "airport",
        "options": list(map(lambda x: {"value": x[0], "label": x[0] + ": " + x[1]},project.get_airports())),
        "action_id": "register"
        }
    ]

    controls = [{
        "type": "button",
        "id": "register",
        "label": "Register"
    }]

    outputs = [{
        "type": "html",
        "id": "register",
        "on_page_load": False
        },
        {
        "type": "html",
        "id": "welcome",
        "on_page_load": False
        }
    ]

    def register(self, params):
        errors = []
        email = params["email"]
        password = params["password"]
        first_name = params['first']
        last_name = params['last']
        airport = params['airport']

        if not email:
            errors.append('Email field is empty')
        if not password:
            errors.append('Password field is empty')
        if not first_name:
            errors.append('First name field is empty')
        if not last_name:
            errors.append('Last name field is empty')
        if not airport:
            errors.append('Airport field is empty')
        if email and password and first_name and last_name and airport:
            if project.register(email, first_name, last_name, password, airport):
                self.welcome(first_name + " " + last_name)
                return "Success"
            else:
                errors.append('Registration failed')
        return env.get_template('login.html').render(errors=errors)
    def welcome(self, params):
        return "Welcome " + params

class LoginApp(server.App):
    title = 'Login'

    inputs = [{
        "type": "text",
        "key": "email",
        "label": "email",
        "action_id": "login"
        },
        {
        "type": "text",
        "key": "password",
        "label": "password",
        "action_id": "login"
        }
    ]

    controls = [{
        "type": "button",
        "id": "login",
        "label": "Login"
    }]

    outputs = [{
        "type": "html",
        "id": "login",
        "on_page_load": False
        },
        {
        "type": "html",
        "id": "welcome"
        }
    ]

    def login(self, params):
        errors = []
        email = params["email"]
        password = params["password"]
        if not email:
            errors.append('Email field is empty')
        if not password:
            errors.append('Password field is empty')
        if email and password:
            user = project.login(email, password)
            if user:
                cherrypy.session['user'] = user
                self.welcome(0)
                return "Success"
            else:
                errors.append('Login failed')
        return env.get_template('login.html').render(errors=errors)
    def welcome(self, params):
        if 'user' in cherrypy.session:
            return "<h1>Welcome " + cherrypy.session['user'][2] + " " + cherrypy.session['user'][3] + "</h1>"
        return ""