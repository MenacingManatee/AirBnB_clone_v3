#!/usr/bin/python3
"""DUMMY DOX"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def api_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def api_stats():
    """Returns the status of the API"""
    from models import storage
    return jsonify({
        'states': storage.count('State'),
        'amenities': storage.count('Amenity'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'users': storage.count('User'),
        'cities': storage.count('City')
        })
