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
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify(place.amenity_ids)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify(), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_to_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
