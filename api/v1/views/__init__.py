#!/usr/bin/python3
"""YET ANOTHER DUMMY DOC"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *