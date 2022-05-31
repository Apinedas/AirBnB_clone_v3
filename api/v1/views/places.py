#!/usr/bin/python3
"""Amenity flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def places_by_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [places.to_dict() for places in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<plc_id>', methods=['DELETE'], strict_slashes=False)
def deletes_place_by_id(plc_id):
    place = storage.get(Place, plc_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify(), 200


@app_views.route(
    'cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_dict = request.get_json()
    if not place_dict:
        abort(400, 'Not a JSON')

    if 'user_id' not in place_dict.keys():
        abort(400, 'Missing user_id')

    valid_user = storage.get(User, place_dict['user_id'])
    if not valid_user:
        abort(404)

    if 'name' not in place_dict.keys():
        abort(400, 'Missing name')

    new_place = Place(**place_dict)
    setattr(new_place, 'city_id', city_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_by_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
