from flask_login import login_user, login_required, logout_user

from app import app, db, login_manager
import models
from generic_requests.GenericRequest import GenericRequest
from flask import request, Response, jsonify
from models import user, professor
from models.user import User, UserPasswordSchema, UserSchema
from util.basic_request_functions import get_all_post, put_delete_get_by_id
from generic_requests.ManyToOneRequest import ManyToOneRequest

requester = ManyToOneRequest(user.User,
                             user.UserSchema(),
                             professor.Professor,
                             user.UserProfSchema(),
                             'professor_id',
                             has_reqparse=True)


@app.route('/users', methods=['GET', 'POST'])
def user_request():
    """
    Processes SignIn request for get or post
    GET will return a list of the information of all SignIn
    POST requires a JSON object containing the studentID under the name of model_id
    :return:
    """
    return get_all_post(requester, request)


@app.route('/users/<id>', methods=['GET', 'DELETE', 'PUT',])
def user_request_by_id(id):
    """
    Preforms put, delete, or get request by student id
    :param id: ID of sign_in
    :return: sign_in data if get, else status code
    """
    return put_delete_get_by_id(requester, request, id)


@app.route('/user_by_prof/<id>', methods=['GET'])
def get_all_user_by_prof(id):
    """
    Gets all sign ins by a student
    :param id: student id
    :return: list of jsons, where each json contains a student and their coresponding sign in
    """
    return requester.get_all_joined_by_one_model_id(id)


@app.route('/login', methods=['POST'])
def log_in():
    email = request.json['email']
    password = request.json['password']
    user = get_user_by_email(email)
    user_info = UserPasswordSchema().dump(user)
    if len(user_info) != 0 and password == user_info['password']:
        login_user(user)
        return {'Message':'Login Successful', 'StatusCode':200}
    return {'Message':'Invalid email or password', 'StatusCode':401}


@app.route('/logout', methods=['POST'])
@login_required
def log_out():
    logout_user()
    return {'Message':'Logout Successful', 'StatusCode':200}


@login_manager.user_loader
def get_user_by_email(email):
    """
    gets the user by email
    :param email: Email of user
    :return: json of user
    """
    #query_result = db.session.query(User).filter(User.email == email).all()
    query_result = User.query.get_or_404(email)
    return query_result
