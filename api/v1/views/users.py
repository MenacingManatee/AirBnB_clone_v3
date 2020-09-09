#!/usr/bin/python3
"""Cities"""
from flask import jsonify, request, abort
from api.v1.views import app_views

@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def api_users(user_id=None):
    """Retrives, deletes, creates and updates a User object"""
    from models import storage
    from models.user import User
    method = request.method

    if method == 'GET':
        if user_id is None:
            users = storage.all(User).values
            return jsonify([user.to_dict() for user in users])
        else:
            obj = storage.get(User, user_id)
            return abort(404) if obj is None else jsonify(obj.to_dict())
    elif method == 'DELETE':
        if user_id is None or storage.get(User, user_id) is None:
            abort(404)
        else:
            storage.delete(User, user_id)
            storage.save()
            return jsonify({})
    elif method == 'POST':
        if request.is_json:
            json = request.get_json()
            if 'email' not in json.keys():
                abort(400, 'Missing email')
            elif 'password' not in json.keys():
                abort(400, 'Missing password')
            else:
                user = User(**json)
                user.save()
                return jsonify(user.to_dict()), 201
        else:
            abort(400, 'Not a JSON')
    elif method == 'PUT':
        user = storage.get(User, user_id)
        if user_id is None or user is None:
            abort(404)
        if request.is_json:
            json = request.get_json()
            for key, value in json.items():
                setattr(user, key, val)
            user.save()
            return jsonify(user.to_dict())
        else:
            abort(404, 'Not a JSON')
