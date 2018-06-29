#!/usr/bin/env python
from flaskexample import app

#app.run(ssl_context('cert.pem','key.pem'), debug=True)
app.run(host='0.0.0.0', debug=True)

