from spyre.server import Site, App
from register_app import LoginApp, RegisterApp
from booking_app import FindFlightsApp, NewBookingApp, CancelBookingApp
from payment_app import NewPaymentApp, EditPaymentApp, DeletePaymentApp
from address_app import NewAddressApp, EditAddressApp, DeleteAddressApp
import cherrypy

cherrypy.config.update({"tools.sessions.on": True})

site = Site(LoginApp)

site.addApp(RegisterApp, '/register')
site.addApp(FindFlightsApp, '/find_flights')
site.addApp(NewBookingApp, '/new_booking')
site.addApp(CancelBookingApp, '/cancel_booking')

site.addApp(NewPaymentApp, '/new_payment')
site.addApp(EditPaymentApp, '/edit_payment')
site.addApp(DeletePaymentApp, '/delete_payment')

site.addApp(NewAddressApp, '/new_address')
site.addApp(EditAddressApp, '/edit_address')
site.addApp(DeleteAddressApp, '/delete_address')

site.launch()