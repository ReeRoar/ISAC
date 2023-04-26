from flask_login import login_required

from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response, jsonify
from marshmallow import ValidationError
from models import attendance_count
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from markupsafe import escape


requester = GenericRequest(attendance_count.AttendanceCount, attendance_count.AttendanceCountSchema(), 'id', True)


@app.route('/attendance_count', methods=['GET', 'POST'])
def attendance_count_request():
    """
    Processes student request for get or post
    GET will return a list of the information of all objects
    POST requires a JSON object contain courses start_time, id, and end_time
    :return:
    """
    return get_all_post(requester, request)


@app.route('/attendance_count/<id>', methods=['GET', 'PUT', 'DELETE'])
def attendance_count_request_by_id(id):
    """
    Preforms put, delete, or get request by object id
    :param id: ID of object
    :return: object data if get, else status code
    """
    if request.method == 'PUT':
        try:
            model_id = escape(id)
            model = attendance_count.AttendanceCount.query.get_or_404(model_id)
            parser = attendance_count.AttendanceCountSchema().get_parser()
            args = parser.parse_args()
            for key, value in args.items():
                if args[key] is not None:
                    setattr(model, key, value)
                    if key == 'camera_value':
                        if value != model.rfid_value:
                            model.mismatch_counter += 1
                        else:
                            model.mismatch_counter = 0
            db.session.commit()
            return jsonify(success=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422

    if request.method == 'GET':
        return requester.get_by_id(id)
    if request.method == 'DELETE':
        return requester.delete_request(id)