from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import professor
from util.basic_request_functions import get_all_post, put_delete_get_by_id


requester = GenericRequest(professor.Professor, professor.ProfessorSchema(), db, True)


@app.route('/professors', methods=['GET', 'POST'])
def professor_request():
    """
    Processes professor request for get or post
    GET will return a list of the information of all professors
    POST requires a JSON object contain student first_name, last_name, id, and email
    :return:
    """
    return get_all_post(requester, request)


@app.route('/professors/<id>', methods=['GET', 'DELETE', 'PUT',])
def professor_request_by_id(id):
    """
    Preforms put, delete, or get request by professor id
    :param id: ID of professor
    :return: professor data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)