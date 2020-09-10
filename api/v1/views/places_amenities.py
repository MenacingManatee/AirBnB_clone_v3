#!/usr/bin/python3
"""DUMMY DOX"""
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def manipulate_places_amenity(place_id, amenity_id=None):
    '''Retrieves, deletes, creates, and updates an Amenity object'''
    from models import storage
    from models.amenity import Amenity
    from models.place import Place
    method = request.method
    if method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    elif method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is None or amenity_id is None:
            abort(404)
        elif place.amenities.get(amenity_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(Amenity, amenity_id))
            del place.amenities[amenity_id]
            storage.save()
            return jsonify({})
    elif method == 'POST':
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        if place is None or amenity is None:
            abort(404)
        if amenity_id in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
            place.save()
            return jsonify(amenity.to_dict()), 201
