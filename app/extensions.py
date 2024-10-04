from flask_restx import Api

from jmorphy import Morphy


api = Api(version='1.0', title='Morphy API',
          description='A Morphy API names modification Library ')
morphy = Morphy()