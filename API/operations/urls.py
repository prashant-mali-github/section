from flask_restful import Api
from flask import Blueprint
from operations.views import OperationResource

from flask_cors import CORS

operation_api = Blueprint('operation_api', __name__)
CORS(operation_api)

api = Api(operation_api)
api.add_resource(OperationResource, '/operations/', '/operations/<int:operation_id>')
