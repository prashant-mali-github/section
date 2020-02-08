import sys
from flask import request,Response,jsonify
from flask_restful import Resource
from sections.serilizers import SectionSchema
from models.db import Roles, Sections
from app import db
import json
import logging
import traceback
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
# from app import spec

sections_schema = SectionSchema(many=True)
section_schema = SectionSchema()

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


class SectionResource(Resource):

    def get(self,section_id=None):
        if section_id:
            section = Sections.query.filter_by(section_id=section_id).first()
            if not section:
                return {"err_msg": "section id does not exit"}
            else:
                result_obj = section_schema.dump(section).data
                return {'status': 'success', 'section': result_obj}, 200
        else:
            sections = Sections.query.all()
            sections = sections_schema.dump(sections).data
            # with open("customers/Customers.json", "w") as f:
            #     print("Success")
            #     f.write(json.dumps("........Register Customers Details..........") \
            #     + ",\n" + json.dumps(customers, indent=4,sort_keys=False) + ",\n")
            return {'status': 'success', 'sections': sections}, 200


    def post(self):

        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        section_data = data.get('section', None)
        if not section_data:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        data, errors = section_schema.load(section_data)
        if errors:
            return {"status": "error", "data": errors}, 422
        try:
            section_title = data['section_title']
            section_description = data['section_description']
            is_active = data['is_active']
            print(section_data)
            section = Sections(section_title, section_description, is_active)
            db.session.add(section)
            db.session.commit()
            result_obj = section_schema.dump(section).data
            response_obj.data = json.dumps(result_obj)
            return response_obj
        except:
            print("Oops!",sys.exc_info()[0],"occured.")

    def put(self, section_id):
        response_obj = Response(mimetype='application/json')
        data = get_request_data(request)
        section_data = data.get('section',
                             None)
        if not section_data:
            response_obj.data = json.dumps({
                "err_msg": "section details are not provided!"
            })
            response_obj.status_code = 400

        else:
            try:
                data, errors = section_schema.load(section_data)

                section = Sections.query.get(int(section_id))
                if not section:
                    logger.error("Edit section: Section doesn't exists! ")
                    response_obj.data = json.dumps({
                        "err_msg": "section id doesn't exists!"
                    })
                else:
                    section.section_title = data['section_title']
                    section.section_description = data['section_description']
                    section.is_active = data['is_active']
                    db.session.add(section)
                    db.session.commit()
                    result_obj = section_schema.dump(section).data
                    logger.info("Edit Section: Section updated successfully.")
                    print("Role edited:")
                    response_obj.data = json.dumps({"Section":result_obj})
                    response_obj.status_code = 200

            except NotFound as ne:
                logger.error("Edit Section: Error while editing section record. " + str(ne))
                response_obj.data = json.dumps({
                    "err_msg": "section doesn't exists!"
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
                    "err_msg": "Error while updating section record!"
                })
                response_obj.status_code = 400

            except Exception:
                response_obj.data = json.dumps({
                    "err_msg": "Error while updating section record!"
                })
                response_obj.status_code = 400

        return response_obj


    def delete(self, section_id):
        response_obj = Response(mimetype='application/json')
        try:
            section = Sections.query.get_or_404(int(section_id))
            db.session.delete(section)
            db.session.commit()
            logger.info("Delete Section: section deleted successfully.")
            response_obj.data = json.dumps({"msg":"section deleted successfully"})
            print("role deleted")
            response_obj.status_code = 200

        except NotFound as ne:
            logger.error("Delete role: Error while deleting  record. " + str(ne))
            response_obj.data = json.dumps({
                "err_msg": "section id doesn't exists!"
            })
            response_obj.status_code = 404

        except DatabaseError as de:
            logger.error("Delete role: Error while deleting role record. " + str(de))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting section record!"
            })
            response_obj.status_code = 400

        except Exception as e:
            logger.error("Delete role: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            response_obj.data = json.dumps({
                "err_msg": "Error while deleting section record!"
            })
            response_obj.status_code = 400
        return response_obj

