from spyre import server
import jinja2
import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(searchpath=ROOT_DIR)
env = jinja2.Environment(loader=templateLoader)

class NewAddressApp(server.App):
    title = 'New Address'

    def getHTML(self, params):
        return ''

class EditAddressApp(server.App):
    title = 'Edit Address'

    def getHTML(self, params):
        return ''

class DeleteAddressApp(server.App):
    title = 'Delete Address'

    def getHTML(self, params):
        return ''