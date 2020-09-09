#!/usr/bin/python3
"""DUMMY DOX"""
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def view_places(city_id):
    '''Returns all places in a city'''
    from models import storage
    from models.city import City
    from models.place import Place
    method = request.method
    if method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        places = city.places
        return jsonify([place.to_dict() for place in places])
    elif method == 'POST':
        if request.is_json:
            jsn = request.get_json()
            if storage.get(City, city_id) is None:
                abort(404)
            jsn.update({"city_id": city_id})
            if 'user_id' in jsn.keys():
                if storage.get(jsn.get(User, 'user_id')) is not None:
                    if 'name' in jsn.keys():
                        place = Place(**jsn)
                        place.save()
                        return jsonify(place.to_dict()), 201
                    else:
                        abort(400, 'Missing name')
                else:
                    abort(404)
            else:
                abort(400, 'Missing user_id')
        else:
            abort(400, 'Not a JSON')


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def manipulate_places(city_id=None):
    '''Retrieves, deletes, creates, and updates a Place object'''
    from models import storage
    from models.place import Place
    method = request.method
    if method == 'GET':
        if place_id is None or storage.get(Place, place_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(Place, place_id).to_dict())
    elif method == 'DELETE':
        if place_id is None or storage.get(Place, place_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(Place, place_id))
            storage.save()
            return jsonify({})
    elif method == 'PUT':
        place = storage.get(Place, place_id)
        if place_id is None or place is None:
            abort(404)
        if request.is_json:
            jsn = request.get_json()
            for key, val in jsn.items():
                if key not in ["id", "user_id", "city_id", "created_at",
                               "updated_at"]:
                    setattr(place, key, val)
            place.save()
            return jsonify(place.to_dict())
        else:
            abort(400, 'Not a JSON')
