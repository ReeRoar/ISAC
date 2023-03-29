from flask import Response
from app import db
from generic_requests.GenericRequest import GenericRequest


def get_all_post(requester, request):
    """
    Defines a simple get all/post request
    :param requester: Object to preform requests
    :param request: request from http
    :return: GET requests will return list of the model, POST requests return a status message
    """
    if request.method == 'GET':
        return requester.get_all()
    if request.method == 'POST':
        return requester.post_request(request)
    return Response('Invalid Request Type', status=400,)


def delete_get_by_id(requester, request, id):
    """
    Deletes or gets by ID
    :param requester: Object to preform requests
    :param request: request from http
    :param id: ID in which the request is being made from
    :return: GET returns the student with matching id, delete returns status code
    """
    if request.method == 'GET':
        return requester.get_by_id(id)
    if request.method == 'DELETE':
        return requester.delete_request(id)


def put_delete_get_by_id(requester, request, id):
    """
    Deletes, puts or gets by ID
    PUTS requires JSON to be passed in request
    :param requester: Object to preform requests
    :param request: request from http
    :param id: ID in which the request is being made from
    :return: If get returns the model with the matching id, else returns status code
    """
    if request.method == 'PUT':
        return requester.put_request(id)
    return delete_get_by_id(requester, request,id)
