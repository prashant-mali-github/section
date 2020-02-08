from flask import request,Response,jsonify
from flask_restful import Resource
from roles.serilizer import RolesSchema
from models.db import Roles
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
# from app import spec

roles_schema = RolesSchema(many=True)
role_schema = RolesSchema()

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


class RolesResource(Resource):

    def get(self,role_id=None):
        if role_id:
            role = Roles.query.filter_by(role_id=role_id).first()
            if not role:
                return {"err_msg": "role id does not exit"}
            else:
                result_obj = role_schema.dump(role).data
                return {'status': 'success', 'role': result_obj}, 200
        else:
            roles = Roles.query.all()
            roles = roles_schema.dump(roles).data
            # with open("customers/Customers.json", "w") as f:
            #     print("Success")
            #     f.write(json.dumps("........Register Customers Details..........") \
            #     + ",\n" + json.dumps(customers, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'roles': roles}, 200


    def post(self):

        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        role_data = data.get('role', None)
        if not role_data:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        data, errors = role_schema.load(role_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        try:
            role_title = data['role_title']
            role_description = data['role_description']
            is_active = data['is_active']
            role = Roles(role_title, role_description, is_active)
            db.session.add(role)
            db.session.commit()
            result_obj = role_schema.dump(role).data
            response_obj.data = json.dumps(result_obj)
            return response_obj

        except:
            print("Oops!",sys.exc_info()[0],"occured.")

    def put(self, role_id):
        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        role_data = data.get('role',
                             None)
        if not role_data:
            response_obj.data = json.dumps({
                "err_msg": "role details are not provided!"
            })
            response_obj.status_code = 400

        else:
            try:
                data, errors = role_schema.load(role_data)

                role = Roles.query.get(int(role_id))
                if not role:
                    logger.error("Edit role: Role doesn't exists! ")
                    response_obj.data = json.dumps({
                        "err_msg": "Role id doesn't exists!"
                    })
                else:
                    role.role_title = data['role_title']
                    role.role_description = data['role_description']
                    role.is_active = data['is_active']
                    db.session.add(role)
                    db.session.commit()
                    result_obj = role_schema.dump(role).data
                    logger.info("Edit Role: Role updated successfully.")
                    print("Role edited:")
                    response_obj.data = json.dumps({"Role":result_obj})
                    response_obj.status_code = 200

            except NotFound as ne:
                logger.error("Edit User: Error while editing user record. " + str(ne))
                response_obj.data = json.dumps({
                    "err_msg": "App doesn't exists!"
                })
                response_obj.status_code = 404

            except ValueError as ve:
                logger.error("Edit User: Error while editing user record. " + str(ve))
                response_obj.data = json.dumps({
                    "err_msg": "Error processing request! Please check for request parameters."
                })
                response_obj.status_code = 400

            except DatabaseError as de:
                logger.error("Edit User: Error while updating user record. " + str(de))
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating user record!"
                })
                response_obj.status_code = 400

            except Exception:
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating user record!"
                })
                response_obj.status_code = 400

        return response_obj


    def delete(self, role_id):
        response_obj = Response(mimetype='application/json')
        try:
            role = Roles.query.get_or_404(int(role_id))
            db.session.delete(role)
            db.session.commit()
            logger.info("Delete Role: Role deleted successfully.")
            response_obj.data = json.dumps({"msg":"role deleted successfully"})
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

