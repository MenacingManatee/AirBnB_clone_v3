#!/usr/bin/python3
"""DUMMY DOX"""
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def manipulate_state(state_id=None):
    '''Retrieves, deletes, creates, and updates a State object'''
    from models import storage
    from models.state import State
    method = request.method
    if method == 'GET':
        if state_id is None:
            states = storage.all(State).values()
            return jsonify([state.to_dict() for state in states])
        elif storage.get(State, state_id) is None:
            abort(404)
        else:
            return jsonify(storage.get(State, state_id).to_dict())
    elif method == 'DELETE':
        if state_id is None or storage.get(State, state_id) is None:
            abort(404)
        else:
            storage.delete(storage.get(State, state_id))
            return jsonify({})
    elif method == 'POST':
        if request.is_json:
            jsn = request.get_json()
            if 'name' in jsn.keys():
                state = State(**jsn)
                state.save()
                return jsonify(state.to_dict()), 201
            else:
                abort(400, 'Missing name')
        else:
            abort(400, 'Not a JSON')
    elif method == 'PUT':
        state = storage.get(State, state_id)
        if state_id is None or state is None:
            abort(404)
        if request.is_json:
            jsn = request.get_json()
            for key, val in jsn.items():
                setattr(state, key, val)
            state.save()
            return jsonify(state.to_dict())
        else:
            abort(400, 'Not a JSON')
