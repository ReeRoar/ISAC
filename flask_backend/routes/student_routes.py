from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import student
from util.basic_request_functions import get_all_post, put_delete_get_by_id


requester = GenericRequest(student.Student, student.StudentSchema(), True)
@app.route('/students', methods=['GET', 'POST'])
def student_request():
    """
    Processes student request for get or post
    GET will return a list of the information of all students
    POST requires a JSON object contain student first_name, last_name, id, and email
    :return:
    """
    return get_all_post(requester, request)


@app.route('/students/<id>', methods=['GET', 'DELETE', 'PUT',])
def student_request_by_id(id):
    """
    Preforms put, delete, or get request by student id
    :param id: ID of student
    :return: student data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)
