from flask_restful import Api
from flask import Blueprint
from sections.views import SectionResource

from flask_cors import CORS

section_api = Blueprint('section_api', __name__)
CORS(section_api)

api = Api(section_api)
api.add_resource(SectionResource, '/sections/', '/sections/<int:section_id>')
