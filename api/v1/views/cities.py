#!/usr/bin/python3
"""DUMMY DOX"""
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def view_cities(state_id):
    '''Returns all cities in a state'''
    from models import storage
    from models.state import State
    from models.city import City
    method = request.method
    if method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])
    elif method == 'POST':
        if request.is_json:
            jsn = request.get_json()
            if storage.get(State, state_id) is None:
                abort(404)
            jsn.update({"state_id": state_id})
            if 'name' in jsn.keys():
                city = City(**jsn)
                city.save()
                return jsonify(city.to_dict()), 201
            else:
                abort(400, 'Missing name')
        else:
            abort(400, 'Not a JSON')


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def manipulate_city(city_id=None):
    '''Retrieves, deletes, creates, and updates a City object'''
    from models import storage
    from models.state import City
    method = request.method
    if method == 'GET':
        if city_id is None or storage.get(City, city_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(City, city_id).to_dict())
    elif method == 'DELETE':
        if city_id is None or storage.get(City, city_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(City, city_id))
            storage.save()
            return jsonify({})
    elif method == 'PUT':
        city = storage.get(City, city_id)
        if city_id is None or city is None:
            abort(404)
        if request.is_json:
            jsn = request.get_json()
            for key, val in jsn.items():
                setattr(city, key, val)
            city.save()
            return jsonify(city.to_dict())
        else:
            abort(400, 'Not a JSON')
