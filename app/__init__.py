from flask import Flask

app = Flask(__name__)

from app import routes

app.run(debug=True, ssl_context='adhoc', host='0.0.0.0')