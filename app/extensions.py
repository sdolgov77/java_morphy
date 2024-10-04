from flask_restx import Api

from jmorphy import Morphy


api = Api(version='1.0', title='Morphy API',
          description='A Morphy API names modification Library ')
morphy = Morphy()

def del_none(source_dict):
    return {key:value for (key, value) in source_dict.items() if value != None}