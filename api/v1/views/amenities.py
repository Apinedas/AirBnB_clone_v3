#!/usr/bin/python3
"""Amenity flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    amenties = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenties)


@app_views.route('/amenities/<amnt_id>', methods=['GET'], strict_slashes=False)
def amenity_by_id(amnt_id):
    amenity = storage.get(Amenity, amnt_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route(
    '/amenities/<amnt_id>', methods=['DELETE'], strict_slashes=False)
def deletes_amenity_by_id(amnt_id):
    amenity = storage.get(Amenity, amnt_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify(), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    new_amenity_dict = request.get_json()
    if not new_amenity_dict:
        abort(400, 'Not a JSON')
    if 'name' not in new_amenity_dict.keys():
        abort(400, 'Missing name')
    new_amenity = Amenity(**new_amenity_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amnt_id>', methods=['PUT'], strict_slashes=False)
def update_amenity_by_id(amnt_id):
    amenity = storage.get(Amenity, amnt_id)
    if not amenity:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
