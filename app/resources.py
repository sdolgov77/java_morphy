from flask_restx import Resource, Namespace

from .api_models import fio_parser, full_fio_parser, dept_parser, post_parser, date_parser
from .extensions import api, morphy


ns = Namespace('api', description='API')


@ns.route('/fio')
class FioApi(Resource):
    @api.doc(parser=fio_parser)
    def get(self):
        args = fio_parser.parse_args()
        
        return morphy.fio(**args)

@ns.route('/fio_full')
class FioApi(Resource):
    @api.doc(parser=full_fio_parser)
    def get(self):
        args = full_fio_parser.parse_args()
        
        return morphy.fio_full(**args)
    
@ns.route('/dept')
class FioApi(Resource):
    @api.doc(parser=dept_parser)
    def get(self):
        args = dept_parser.parse_args()
        
        return morphy.dept(**args)    
    
@ns.route('/post')
class FioApi(Resource):
    @api.doc(parser=post_parser)
    def get(self):
        args = post_parser.parse_args()
        
        return morphy.post(**args)     
    
@ns.route('/print_date')
class FioApi(Resource):
    @api.doc(parser=date_parser)
    def get(self):
        args = date_parser.parse_args()
        
        return morphy.print_date(**args)      