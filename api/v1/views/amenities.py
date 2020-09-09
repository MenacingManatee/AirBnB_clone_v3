#!/usr/bin/python3
"""DUMMY DOX"""
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def manipulate_amenity(amenity_id=None):
    '''Retrieves, deletes, creates, and updates an Amenity object'''
    from models import storage
    from models.amenity import Amenity
    method = request.method
    if method == 'GET':
        if amenity_id is None:
            amenities = storage.all(Amenity).values()
            return jsonify([amenity.to_dict() for amenity in amenities])
        elif storage.get(Amenity, amenity_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(Amenity, amenity_id).to_dict())
    elif method == 'DELETE':
        if amenity_id is None or storage.get(Amenity, amenity_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(Amenity, amenity_id))
            storage.save()
            return jsonify({})
    elif method == 'POST':
        if request.is_json:
            jsn = request.get_json()
            if 'name' in jsn.keys():
                amenity = Amenity(**jsn)
                amenity.save()
                return jsonify(amenity.to_dict()), 201
            else:
                abort(400, 'Missing name')
        else:
            abort(400, 'Not a JSON')
    elif method == 'PUT':
        amenity = storage.get(Amenity, amenity_id)
        if amenity_id is None or amenity is None:
            abort(404)
        if request.is_json:
            jsn = request.get_json()
            for key, val in jsn.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(amenity, key, val)
            amenity.save()
            return jsonify(amenity.to_dict())
        else:
            abort(400, 'Not a JSON')
