#!/usr/bin/python3
"""Amenities by Places flask handler"""

import json
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    'places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def places_amenities(place_id):

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if storage_t == 'db':
        return jsonify(place.amenities)
    else:
        return jsonify(place.amenity_ids)
