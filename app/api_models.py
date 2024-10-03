from flask_restx import fields, reqparse

from .extensions import api
from jmorphy.settings import RegimeLength, Case

test_model = api.model('Test', {
    'test': fields.String,
    'test2': fields.Integer
})

parser = reqparse.RequestParser()
parser.add_argument("ip", type=str, required=True, help="Example - [10.10.100.5]", location="args")
parser.add_argument("netmask", type=str, required=True, help="Example - [255.255.255.0]", location="args")
parser.add_argument("vrf", type=str, required=True, help="Example - [Global, Admin, DMZ]", location="args")
parser.add_argument("status", type=str, required=True, help="Example - [Available, Reserved, Used]", location="args")
parser.add_argument("status", type=str, required=True, choices=[v.value for v in RegimeLength], help="Example - reverse_short", location="args")