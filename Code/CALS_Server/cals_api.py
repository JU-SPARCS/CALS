!/usr/bin/python

import falcon

from cals_routes import *

app = falcon.API()

api = apiResource()

app.add_route('/login', api)
app.add_route('/logout', api)
app.add_route('/roleChange', api)
