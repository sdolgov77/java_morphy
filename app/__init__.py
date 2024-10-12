from flask import Flask

from .extensions import api
from .resources import ns

app = Flask(__name__)

api.init_app(app)
api.add_namespace(ns)

# def create_app(*args, **kwargs):
#     app = Flask(__name__)

#     api.init_app(app)
#     api.add_namespace(ns)

#     return app
