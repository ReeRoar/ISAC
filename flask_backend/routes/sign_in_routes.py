from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import sign_in, student
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from generic_requests.ManyToOneRequest import ManyToOneRequest

requester = ManyToOneRequest(sign_in.SignIn, sign_in.SignInSchema(), db, student.Student, sign_in.StudentSignInSchema(), has_reqparse=True)


@app.route('/sign_ins', methods=['GET', 'POST'])
def sign_in_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the studentID under the name of model_id
    :return:
    """
    return get_all_post(requester, request)


@app.route('/sign_ins/<id>', methods=['GET', 'DELETE', 'PUT',])
def sign_in_request_by_id(id):
    """
    Preforms put, delete, or get request by student id
    :param id: ID of sign_in
    :return: sign_in data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)


@app.route('/student_sign_ins/<id>', methods=['GET'])
def get_all_sign_ins_by_student(id):
    return requester.get_all_joined_by_one_model_id(id)

