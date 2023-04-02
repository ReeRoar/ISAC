from flask_login import login_required

from app import app, db
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import professor_assignment, professor, course
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from generic_requests.ManyToManyRequest import ManyToManyRequest

requester = ManyToManyRequest(professor_assignment.ProfessorAssignment,
                              professor_assignment.ProfessorAssignmentSchema(),
                              professor_assignment.ProfessorAssignmentJoinedSchema(),
                              professor.Professor,
                              course.Course,
                              "professor_id",
                              "course_number")


@login_required
@app.route('/prof_assignment', methods=['GET', 'POST'])
def prof_assignment_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the model_id for the prof id, and model2_id for the course id
    :return:
    """
    return get_all_post(requester, request)


@login_required
@app.route('/prof_assignment/<id>', methods=['GET', 'DELETE', 'PUT', ])
def prof_assignment_request_by_id(id):
    """
    Preforms put, delete, or get request by object id
    :param id: ID of object
    :return: object data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)


@login_required
@app.route('/prof_assignment_id/<id>', methods=['GET'])
def prof_assignment_by_prof_id(id):
    """
    Gets all sign ins by a student
    :param id: prof id
    :return: list of jsons, containing the joined values of professor and courses
    """
    return requester.get_all_joined_by_model_id(id)
