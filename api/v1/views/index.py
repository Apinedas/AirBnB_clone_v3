#!/usr/bin/python3
"""Index file for Flask blueprints"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def ret_status():
    return(jsonify(status="OK"))
