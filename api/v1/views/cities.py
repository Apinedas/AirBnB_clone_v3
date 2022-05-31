#!/usr/bin/python3
"""City flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<st_id>/cities', methods=['GET'], strict_slashes=False)
def cities_by_state(st_id):
    state = storage.get(State, st_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletes_city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify(), 200


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    if not storage.get(State, state_id):
        abort(404)
    new_city_dict = request.get_json()
    if not new_city_dict:
        abort(400, 'Not a JSON')
    if 'name' not in new_city_dict.keys():
        abort(400, 'Missing name')
    new_state = City(**new_city_dict)
    setattr(new_state, 'state_id', state_id)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
