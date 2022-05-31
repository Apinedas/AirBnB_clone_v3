#!/usr/bin/python3
"""User flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_users():
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<usr_id>', methods=['GET'], strict_slashes=False)
def user_by_id(usr_id):
    user = storage.get(User, usr_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deletes_user_by_id(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify(), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    new_user_dict = request.get_json()
    if not new_user_dict:
        abort(400, 'Not a JSON')
    if 'email' not in new_user_dict.keys():
        abort(400, 'Missing email')
    if 'password' not in new_user_dict.keys():
        abort(400, 'Missing password')
    new_user = User(**new_user_dict)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(usr_id):
    user = storage.get(User, usr_id)
    if not user:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue
        else:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
