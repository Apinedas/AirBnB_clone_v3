#!/usr/bin/python3
"""State flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def retrieves_states():
    ret_list = []
    for state in storage.all(State).values():
        ret_list.append(state.to_dict())
    return jsonify(ret_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def retrieves_state_by_id(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deletes_state_by_id(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            state.delete()
            return jsonify(), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    new_state_dict = request.get_json()
    if not new_state_dict:
        abort(400, 'Not a JSON')
    if 'name' not in new_state_dict.keys():
        abort(400, 'Missing name')
    new_state = State(**new_state_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_by_id(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            ommited = ['id', 'created_at', 'updated_at']
            update_dict = request.get_json()
            if not update_dict:
                abort(400, 'Not a JSON')
            for key, value in update_dict.items():
                if key not in ommited:
                    state.__dict__[key] = value
            state.save()
            return jsonify(state.to_dict()), 200
    abort(404)
