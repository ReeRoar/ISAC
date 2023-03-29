from app import app
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response
from models import student_enrollment, course, student
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from generic_requests.ManyToManyRequest import ManyToManyRequest

requester = ManyToManyRequest(student_enrollment.StudentEnrollment,
                              student_enrollment.StudentEnrollmentSchema(),
                              student_enrollment.StudentEnrollmentJoinedSchema(),
                              student.Student,
                              course.Course,
                              'student_id',
                              'course_number')


@app.route('/student_enroll', methods=['GET', 'POST'])
def student_enroll_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the model_id for the student id, and model2_id for the course id
    :return:
    """
    return get_all_post(requester, request)


@app.route('/student_enroll/<id>', methods=['GET', 'DELETE', 'PUT', ])
def student_enroll_request_by_id(id):
    """
    Preforms put, delete, or get request by object id
    :param id: ID of object
    :return: object data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)


@app.route('/student_enroll_course_id/<id>', methods=['GET'])
def student_enroll_course_id(id):
    """
    Gets all sign ins by a course id
    :param id: course id
    :return: list of jsons, containing the joined values of students and courses
    """
    return requester.get_all_joined_by_model2_id(id)
