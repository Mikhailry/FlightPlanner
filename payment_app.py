from spyre import server
import jinja2
import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=ROOT_DIR)
env = jinja2.Environment(loader=templateLoader)

class NewPaymentApp(server.App):
    title = 'New Payment'

    def getHTML(self, params):
        return ''

class EditPaymentApp(server.App):
    title = 'Edit Payment'

    def getHTML(self, params):
        return ''

class DeletePaymentApp(server.App):
    title = 'Delete Payment'

    def getHTML(self, params):
        return ''