from flask_restx import Resource, Namespace

from .api_models import fio_parser, full_fio_parser, dept_parser, post_parser, \
    date_parser, phrase_parser, count_parser, dept_init_parser, dept_init_lower_parser, init_parser, \
    count_pattern_parser, sum_parser, upper_parser, case_check_parser, regime_check_parser, cut_post_parser
from .extensions import api, morphy, del_none


ns = Namespace('api', description='API')


@ns.route('/fio')
class FioApi(Resource):
    @api.doc(parser=fio_parser)
    def get(self):
        args = fio_parser.parse_args()

        return morphy.fio(**args)


@ns.route('/fio_full')
class FioFullApi(Resource):
    @api.doc(parser=full_fio_parser)
    def get(self):
        args = full_fio_parser.parse_args()

        return morphy.fio_full(**args)


@ns.route('/dept')
class DeptApi(Resource):
    @api.doc(parser=dept_parser)
    def get(self):
        args = dept_parser.parse_args()

        return morphy.dept(**args)


@ns.route('/dept_init')
class DeptInitApi(Resource):
    @api.doc(parser=dept_init_parser)
    def get(self):
        args = dept_init_parser.parse_args()

        return morphy.dept_init(**args)


@ns.route('/dept_init_lower')
class DeptInitLowerApi(Resource):
    @api.doc(parser=dept_init_lower_parser)
    def get(self):
        args = dept_init_lower_parser.parse_args()

        return morphy.dept_init_lower(**args)


@ns.route('/init_lower')
class InitLowerApi(Resource):
    @api.doc(parser=init_parser)
    def get(self):
        args = init_parser.parse_args()

        return morphy.init_lower(**args)


@ns.route('/init_upper')
class InitUpperApi(Resource):
    @api.doc(parser=init_parser)
    def get(self):
        args = init_parser.parse_args()

        return morphy.init_upper(**args)


@ns.route('/post')
class PostApi(Resource):
    @api.doc(parser=post_parser)
    def get(self):
        args = post_parser.parse_args()

        return morphy.post(**args)


@ns.route('/print_date')
class DateApi(Resource):
    @api.doc(parser=date_parser)
    def get(self):
        args = date_parser.parse_args()

        return morphy.print_date(**args)


@ns.route('/phrase')
class PhraseApi(Resource):
    @api.doc(parser=phrase_parser)
    def get(self):
        args = phrase_parser.parse_args()
        _args = del_none(args)
        return morphy.phrase(**_args)


@ns.route('/print_count')
class PrintCountApi(Resource):
    @api.doc(parser=count_parser)
    def get(self):
        args = count_parser.parse_args()
        return morphy.print_count(**args)


@ns.route('/print_count_pattern')
class PrintCountPatternApi(Resource):
    @api.doc(parser=count_pattern_parser)
    def get(self):
        args = count_pattern_parser.parse_args()
        return morphy.print_count_pattern(**args)


@ns.route('/print_sum')
class PrintSumApi(Resource):
    @api.doc(parser=sum_parser)
    def get(self):
        args = sum_parser.parse_args()
        _args = del_none(args)
        return morphy.print_sum(**_args)


@ns.route('/upper')
class UpperApi(Resource):
    @api.doc(parser=upper_parser)
    def get(self):
        args = upper_parser.parse_args()
        return morphy.upper(**args)


@ns.route('/check_phrase_case')
class CheckPhraseCaseApi(Resource):
    @api.doc(parser=case_check_parser)
    def get(self):
        args = case_check_parser.parse_args()
        return morphy.check_phrase_case(**args)


@ns.route('/check_regime_length')
class CheckRegimeLengthApi(Resource):
    @api.doc(parser=regime_check_parser)
    def get(self):
        args = regime_check_parser.parse_args()
        return morphy.check_regime_length(**args)


@ns.route('/check_regime_post')
class CheckRegimePostApi(Resource):
    @api.doc(parser=regime_check_parser)
    def get(self):
        args = regime_check_parser.parse_args()
        return morphy.check_regime_post(**args)


@ns.route('/cut_post')
class CutPostApi(Resource):
    @api.doc(parser=cut_post_parser)
    def get(self):
        args = cut_post_parser.parse_args()
        return morphy.cut_post(**args)
