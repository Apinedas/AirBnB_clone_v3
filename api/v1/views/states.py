#!/usr/bin/python3
"""State flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieves_states():
    ret_list = []
    for state in storage.all(State).values():
        ret_list.append(state.to_dict())
    return jsonify(ret_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieves_state_by_id(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<st_id>', methods=['DELETE'], strict_slashes=False)
def deletes_state_by_id(st_id):
    state = storage.get(State, st_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    new_state_dict = request.get_json()
    if not new_state_dict:
        abort(400, 'Not a JSON')
    if 'name' not in new_state_dict.keys():
        abort(400, 'Missing name')
    new_state = State(**new_state_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
