#!/usr/bin/python3
"""DOCSTRING"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_fs_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def api_error(self):
    """Returns an error page when pinged"""
    return jsonify({ "error": "Not Found" }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
