#!/usr/bin/python3
"""DOCSTRING"""
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_fs_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def api_error(self):
    """Returns an error page when pinged"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    from os import getenv
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = '5000'
    app.run(host=host, port=port, threaded=True, debug=True)
