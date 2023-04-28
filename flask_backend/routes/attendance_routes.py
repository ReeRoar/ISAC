#from flask_login import login_required

from app import app, db #, login_manager
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import attendance, student, course
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from generic_requests.ManyToManyRequest import ManyToManyRequest

requester = ManyToManyRequest(attendance.Attendance,
                              attendance.AttendanceSchema(),
                              attendance.AttendanceJoinedSchema(),
                              student.Student,
                              course.Course,
                              "student_id",
                              "course_number")


@app.route('/attendance', methods=['GET', 'POST'])
def attendance_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the model_id for the student id, and model2_id for the course id
    :return:
    """
    return get_all_post(requester, request)


@app.route('/attendance_student', methods=['GET'])
def attendance_student_list_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the model_id for the student id, and model2_id for the course id
    :return:
    """

    return requester.get_all_joined()


@app.route('/attendance/<id>', methods=['GET', 'DELETE', 'PUT', ])
def attendance_request_by_id(id):
    """
    Preforms put, delete, or get request by object id
    :param id: ID of object
    :return: object data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)


@app.route('/attendance_student/<id>', methods=['GET'])
def attendance_by_student_id(id):
    """
    Gets objects by student id
    :param id: student_id
    :return: list of jsons, containing the joined values of objects
    """
    return requester.get_all_joined_by_model_id(id)

@app.route('/attendance_course/<id>', methods=['GET'])
def attendance_by_course_id(id):
    """
    Gets objects by course id
    :param id: course
    :return: list of jsons, containing the joined values of objects
    """
    return requester.get_all_joined_by_model2_id(id)

