from flask_login import login_required

from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response, jsonify
from marshmallow import ValidationError
from models import sign_in, student
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from generic_requests.ManyToOneRequest import ManyToOneRequest

from models.attendance import Attendance

from models.attendance_count import AttendanceCount

requester = ManyToOneRequest(sign_in.SignIn,
                             sign_in.SignInSchema(),
                             student.Student,
                             sign_in.StudentSignInSchema(),
                             'student_id',
                             has_reqparse=True)


@app.route('/sign_ins', methods=['GET', 'POST'])
def sign_in_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the studentID under the name of model_id
    :return:
    """
    if request.method == 'GET':
        return requester.get_all()
    if request.method == 'POST':
        json_input = request.json
        try:
            #TODO support multiple classes
            data = sign_in.SignInSchema().load(json_input)
            db.session.add(data)
            student_id = json_input['student_id']
            attendance = db.session.query(Attendance).filter(
                getattr(Attendance, "student_id") == student_id,
                getattr(Attendance, "course_number") == 1).first()
            attendance_count = AttendanceCount.query.get_or_404(1)

            if attendance.status == 'Y':
                attendance.status = 'N'
                attendance_count.rfid_value -= 1
            elif attendance.status == 'N':
                attendance.status = 'Y'
                attendance_count.rfid_value += 1
            db.session.commit()
            return jsonify(success=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422


@app.route('/sign_ins/<id>', methods=['GET', 'DELETE', 'PUT',])
@login_required
def sign_in_request_by_id(id):
    """
    Preforms put, delete, or get request by student id
    :param id: ID of sign_in
    :return: sign_in data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)


@app.route('/student_sign_ins/<id>', methods=['GET'])
@login_required
def get_all_sign_ins_by_student(id):
    """
    Gets all sign ins by a student
    :param id: student id
    :return: list of jsons, where each json contains a student and their coresponding sign in
    """
    return requester.get_all_joined_by_one_model_id(id)

