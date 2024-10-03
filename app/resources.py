from flask_restx import Resource, Namespace

from .api_models import test_model, parser
from .extensions import api


ns = Namespace('api', description='API')


@ns.route('/test_api')
class TestApi(Resource):
    @api.doc(parser=parser)
    @ns.marshal_with(test_model)
    def get(self):
        args = parser.parse_args()
        
        return {'test': 'test', 'test2': 2}

