from flask_restful import Api
from flask import Blueprint
from rolesconfig.views import RoleConfigResource

from flask_cors import CORS

roles_config_api = Blueprint('roles_config_api', __name__)
CORS(roles_config_api)

api = Api(roles_config_api)
api.add_resource(RoleConfigResource, '/rolesconfig/', '/rolesconfig/<int:role_config_id>')
