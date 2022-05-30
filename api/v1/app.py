#!/usr/bin/python3
"""First blueprint for HBNB Project"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
