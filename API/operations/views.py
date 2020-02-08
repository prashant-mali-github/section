import sys
from flask import request,Response,jsonify
from flask_restful import Resource
from operations.serilizers import SectionSchema, OperationSchema
from models.db import Roles, Sections, Operations
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
# from app import spec

operations_schema = OperationSchema(many=True)
operation_schema = OperationSchema()

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


class OperationResource(Resource):

    def get(self,operation_id=None):
        if operation_id:
            operation = Operations.query.filter_by(operation_id=operation_id).first()
            if not operation:
                return {"err_msg": "operation id does not exit"}
            else:
                result_obj = operation_schema.dump(operation).data
                return {'status': 'success', 'operation': result_obj}, 200
        else:
            operations = Operations.query.all()
            operations = operations_schema.dump(operations).data
            # with open("customers/Customers.json", "w") as f:
            #     print("Success")
            #     f.write(json.dumps("........Register Customers Details..........") \
            #     + ",\n" + json.dumps(customers, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'operations': operations}, 200

    def post(self):
        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        operation_data = data.get('operation', None)
        if not operation_data:
            response_obj.data = json.dumps({'message': 'No input data provided'}), 400

        data, errors = operation_schema.load(operation_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        try:
            section = Sections.query.filter_by(section_id=int(data['section_id'])).first()
            if not section:
                response_obj.data = json.dumps({"msg": "please enter valid section ID"})
            else:
                section_id = data['section_id']
                operation_title = data['operation_title']
                operation_description = data['operation_description']
                is_active = data['is_active']
                operation = Operations(section_id, operation_title,operation_description, is_active)
                db.session.add(operation)
                db.session.commit()
                result_obj = operation_schema.dump(operation).data
                response_obj.data = json.dumps(({"status": 'success', "operation": result_obj}))
        except Exception as e:
            print(e)
        return response_obj

    
    def put(self, operation_id):
        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        operation_data = data.get('operation',
                             None)
        print(operation_data)
        if not operation_data:
            response_obj.data = json.dumps({
                "err_msg": "operation details are not provided!"
            })
            response_obj.status_code = 400
        else:
            try:
                data, errors = operation_schema.load(operation_data)
                print(data)
                if errors:
                    return {"status": "error", "data": errors}, 422
                
                operation = Operations.query.filter_by(operation_id=operation_id).first()
                if  not operation:
                    response_obj.data = json.dumps({
                        "err_msg": "operation id doesn't exists!"
                    })

                print(operation)
                section = Sections.query.filter_by(section_id=int(data['section_id'])).first()
                print(section)
                if not section:
                    response_obj.data = json.dumps({
                        "err_msg": "section id doesn't exists!"
                    })
                
                operation.section_id = data['section_id']
                operation.operation_title = data['operation_title']
                operation.operation_description = data['operation_description']
                operation.is_active = data['is_active']
                # print(operation_data)
                db.session.add(operation)
                db.session.commit()
                print("..........")
                result_obj = operation_schema.dump(operation).data
                logger.info("Edit operatioon: operation updated successfully.")
                print("Role edited:")
                response_obj.data = json.dumps({"Operation":result_obj})
                response_obj.status_code = 200

            except:
                print("Oops!",sys.exc_info()[0],"occured.")
        return response_obj


    def delete(self, operation_id):
        response_obj = Response(mimetype='application/json')
        try:
            operation = Operations.query.get_or_404(int(operation_id))
            db.session.delete(operation)
            db.session.commit()
            logger.info("Delete Operation: Operation deleted successfully.")
            response_obj.data = json.dumps({"msg":"operation deleted successfully"})
            response_obj.status_code = 200

        except NotFound as ne:
            logger.error("Delete operation: Error while deleting operation record. " + str(ne))
            response_obj.data = json.dumps({
                "err_msg": "operation id doesn't exists!"
            })
            response_obj.status_code = 404

        except DatabaseError as de:
            logger.error("Delete role: Error while deleting role record. " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Invalid operation id"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete operation: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting operation record!"
            })
            response_obj.status_code = 400
        return response_obj

