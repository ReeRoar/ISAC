from flask_login import login_required

from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import course
from util.basic_request_functions import get_all_post, put_delete_get_by_id


requester = GenericRequest(course.Course, course.CourseSchema(), 'course_number', True)


@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses_request():
    """
    Processes student request for get or post
    GET will return a list of the information of all objects
    POST requires a JSON object contain courses start_time, id, and end_time
    :return:
    """
    return get_all_post(requester, request)


@app.route('/courses/<id>', methods=['GET', 'DELETE', 'PUT',])
@login_required
def courses_request_by_id(id):
    """
    Preforms put, delete, or get request by object id
    :param id: ID of object
    :return: object data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)
