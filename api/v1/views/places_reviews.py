#!/usr/bin/python3
"""Amenity flask handler"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def review_by_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<rvw_id>', methods=['DELETE'], strict_slashes=False)
def deletes_review_by_id(rvw_id):
    review = storage.get(Review, rvw_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify(), 200


@app_views.route(
    'places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    review_dict = request.get_json()
    if not review_dict:
        abort(400, 'Not a JSON')

    if 'user_id' not in review_dict.keys():
        abort(400, 'Missing user_id')

    valid_user = storage.get(User, review_dict['user_id'])
    if not valid_user:
        abort(404)

    if 'text' not in review_dict.keys():
        abort(400, 'Missing text')

    new_review = Review(**review_dict)
    setattr(new_review, 'place_id', place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_by_id(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for key, value in body.items():
        if key in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
