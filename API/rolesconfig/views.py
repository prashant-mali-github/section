import sys
from flask import request,Response,jsonify
from flask_restful import Resource
from roles.serilizer import RolesSchema
from rolesconfig.serilizers import RolesConfigSchema
from models.db import Roles, RoleConfig, Operations
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
# from app import spec

roles_schema = RolesSchema(many=True)
role_schema = RolesSchema()

roles_config_schema = RolesConfigSchema(many=True)
role_config_schema = RolesConfigSchema()

logger = logging.getLogger(__name__)


def get_request_data(request):
    try:
        if request.mimetype == 'application/json':
            data = request.get_json()
        else:
            data = request.form.to_dict()

    except Exception as e:
        logger.error("Request Data: Fetching request data failed! " + str(e))
        return jsonify(err_msg="Error in fetching request data"), 400

    return data


class RoleConfigResource(Resource):

    def get(self,role_config_id=None):
        if role_config_id:
            role_config_id = RoleConfig.query.filter_by(role_config_id=role_config_id).first()
            if not role_config_id:
                return {"err_msg": "role config id does not exit"}
            else:
                result_obj = role_schema.dump(role_config_id).data
                return {'status': 'success', 'role_config': result_obj}, 200
        else:
            roles_configs = RoleConfig.query.all()
            roles_configs = roles_config_schema.dump(roles_configs).data
            # with open("customers/Customers.json", "w") as f:
            #     print("Success")
            #     f.write(json.dumps("........Register Customers Details..........") \
            #     + ",\n" + json.dumps(customers, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'role_config': roles_configs}, 200


    def post(self):
        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        role_config_data = data.get('role_config', None)
        if not role_config_data:
            return {'message': 'No input data provided'}, 400

        data, errors = role_config_schema.load(role_config_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        
        else:
            try:
                role_id = data['role_id']
                operation_id = data['operation_id']
                role = Roles.query.filter_by(role_id=int(data['role_id'])).first()
                if not role:
                    response_obj.data = json.dumps({"msg": "please enter valid role ID"})
                operation = Operations.query.filter_by(operation_id=data['operation_id']).first()
                if not operation:
                    response_obj.data = json.dumps({"msg": "please enter valid operation ID"})
                else:
                    role_config = RoleConfig(role_id, operation_id, data['is_active'])
                    db.session.add(role_config)
                    db.session.commit()
                    print("hello")
                    result_obj = role_config_schema.dump(role_config).data
                    response_obj.data = json.dumps(({"status": 'success', "Role_config": result_obj}))
                return response_obj
            except:
                print("Oops!",sys.exc_info()[0],"occured.")



    def put(self, role_config_id):
        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        role_config_data = data.get('role_config',
                             None)
        print(role_config_data)
        if not role_config_data:
            response_obj.data = json.dumps({
                "err_msg": "role_config details are not provided!"
            })
            response_obj.status_code = 400
        else:
            try:
                data, errors = role_config_schema.load(role_config_data)
                print(data)
                if errors:
                    return {"status": "error", "data": errors}, 422
                role_config = RoleConfig.query.filter_by(role_config_id=role_config_id).first()
                print(role_config)
                if not role_config_id:
                    response_obj.data = json.dumps({
                        "err_msg": "Role_config id doesn't exists!"
                    })
                operation = Operations.query.filter_by(operation_id=int(data['operation_id'])).first()
                print(operation)
                if operation is None:
                    response_obj.data = json.dumps({
                        "err_msg": "operation id doesn't exists!"
                    })
                role = Roles.query.filter_by(role_id=int(data['role_id'])).first()
                print(role)
                if role is None:
                    response_obj.data = json.dumps({
                        "err_msg": "Role id doesn't exists!"
                    })
                role_config.role_id = data['role_id']
                role_config.operation_id = data['operation_id']
                role_config.is_active = data['is_active']
                print(role_config_data)
                db.session.add(role_config)
                db.session.commit()
                result_obj = role_config_schema.dump(role_config).data
                logger.info("Edit Config_Role: Role updated successfully.")
                print("Role edited:")
                response_obj.data = json.dumps({"Role_Config":result_obj})
                response_obj.status_code = 200

            except:
                print("Oops!",sys.exc_info()[0],"occured.")
            # except NotFound as ne:
            #     logger.error("Edit User: Error while editing user record. " + str(ne))
            #     response_obj.data = json.dumps({
            #         "err_msg": "role_config doesn't exists!"
            #     })
            #     response_obj.status_code = 404

            # except ValueError as ve:
            #     logger.error("Edit User: Error while editing user record. " + str(ve))
            #     response_obj.data = json.dumps({
            #         "err_msg": "Error processing request! Please check for request parameters."
            #     })
            #     response_obj.status_code = 400
            # except IntegrityError as ve:
            #     logger.error("Edit User: Error while editing user record. " + str(ve))
            #     response_obj.data = json.dumps({
            #         "err_msg": "Error processing request! Please check for request parameters."
            #     })
            #     response_obj.status_code = 400
            # except DatabaseError as de:
            #     logger.error("Edit User: Error while updating user record. " + str(de))
            #     response_obj.data = json.dumps({
            #         "err_msg": "Error while updating Role_config record!"
            #     })
            #     response_obj.status_code = 400

            # except Exception:
            #     response_obj.data = json.dumps({
            #         "err_msg": "Error while updating role_config record!"
            #     })
            #     print("...........")
            #     response_obj.status_code = 400

        return response_obj


    def delete(self, role_config_id):
        response_obj = Response(mimetype='application/json')
        try:
            role_config = RoleConfig.query.get_or_404(int(role_config_id))
            db.session.delete(role_config)
            db.session.commit()
            logger.info("Delete Role: Role Confiuation deleted successfully.")
            response_obj.data = json.dumps({"msg":"role configuration deleted successfully"})
            print("role deleted")
            response_obj.status_code = 200

        except NotFound as ne:
            logger.error("Delete role: Error while deleting role record. " + str(ne))
            response_obj.data = json.dumps({
                "err_msg": "role id doesn't exists!"
            })
            response_obj.status_code = 404

        except DatabaseError as de:
            logger.error("Delete role: Error while deleting role record. " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting role record!"
            })
            response_obj.status_code = 400
        
        except Exception as e:
            logger.error("Delete role: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting role record!"
            })
            response_obj.status_code = 400
        return response_obj

