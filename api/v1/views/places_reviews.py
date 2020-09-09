#!/usr/bin/python3
"""Place_Reviews Relationship - API"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def api_place_reviews(place_id=None):
    """I dunno"""
    from models.place import Place
    from models.review import Review

    # Get a specific object
    if request.method == 'GET':
        if place_id is not None:
            obj = storage.get(Place, place_id)
            if obj is None:
                abort(404)
            else:
                return jsonify([review.to_dict() for review in obj.reviews])

    # Create a new object from a JSON request
    elif request.method == 'POST':
        if place_id is not None:
            obj = storage.get(Place, place_id)
            if obj is None:
                abort(404)
            if request.is_json:
                incoming_json = request.get_json()
                if 'user_id' not in incoming_json.keys():
                    abort(400, 'Missing user_id')
                elif storage.get(User, incoming_json.get('user_id')) is None:
                    abort(404)
                elif 'text' not in incoming_json.keys():
                    abort(400, 'Missing text')
                incoming_json.update({'place_id': place_id})
                obj = Review(**incoming_json)
                obj.save()
                return jsonify(obj.to_dict())
            else:
                abort(400, 'Not a JSON')


@app_views.route('reviews/<review_id>', methods=['PUT', 'GET', 'DELETE'],
                 strict_slashes=False)
def api_review(review_id=None):
    """Creates/updates a Review object"""
    from models.review import Review
    from models.user import User

    # Retrieve an object
    if request.method == 'GET':
        if review_id is not None:
            obj = storage.get(Review, review_id)
            if obj is None:
                abort(404)
            else:
                return jsonify(obj.to_dict())

    # Delete a specific object
    elif request.method == 'DELETE':
        if review_id is not None:
            obj = storage.get(Review, review_id)
            if obj is None:
                abort(404)
            else:
                storage.delete(obj)
                storage.save()
                return jsonify({})
        else:
            abort(404)

    # Update a specific object
    elif request.method == 'PUT':
        if review_id is not None:
            review = storage.get(Review, review_id)
            if request.is_json:
                excl_attrs = ['id', 'user_id', 'place_id',
                              'created_at', 'updated_at']
                incoming_json = request.get_json()
                for key, value in incoming_json.items():
                    if key not in excl_attrs:
                        setattr(review, key, value)
                review.save()
                return jsonify(review.to_dict())
            else:
                abort(400, 'Not a JSON')
