from flask_restful import Api
from flask import Blueprint
from roles.views import RolesResource

from flask_cors import CORS

roles_api = Blueprint('roles_api', __name__)
CORS(roles_api)

api = Api(roles_api)
api.add_resource(RolesResource, '/roles/', '/roles/<int:role_id>')
