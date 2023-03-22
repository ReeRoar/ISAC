from flask import jsonify, abort
from markupsafe import escape
from marshmallow import (
    ValidationError,
)
from app import db

class GenericRequest:
    def __init__(self, model, schema, has_reqparse=True, id='id'):
        """
        Class in order to make model agnostic requests. This class only contains basic requests and should be extended
        in order to create requests having joined tables.

        :param model: Class in which the requests will be made from
        :param schema: Model Schema
        :param db: database session
        :param has_reqparse: Boolean to represent whether or not this class has a reqparse
        """
        self.schema = schema
        self.model = model
        if has_reqparse:
            self.parser = schema.get_parser()
        self.db = db
        self.id = id
    def get_all(self):
        """
        Gets all rows of model
        :return: list of JSON objects containing each row of the model within the database
        """
        query_result = self.model.query.all()
        return jsonify([self.schema.dump(obj) for obj in query_result])

    def get_by_id(self, id):
        """
        Gets singular object by id
        :param id: primary key of object
        :return: Object in which the id belongs to
        """
        model_id = escape(id)
        model = self.model.query.get_or_404(model_id)
        return jsonify(self.schema.dump(model))

    def put_request(self, id):
        """
        Preforms a put request for given ID
        :param id: value of primary key
        :return: Success status of request
        """
        try:
            model_id = escape(id)
            model = self.model.query.get_or_404(model_id)
            args = self.parser.parse_args()
            for key, value in args.items():
                if args[key] is not None:
                    setattr(model, key, value)
            self.db.session.commit()
            return jsonify(success=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422

    def post_request(self, request):
        """
        preforms a post request to add object to database
        :param request: the HTTP request containing model information
        :return: Success status of request
        """
        json_input = request.json
        try:
            data = self.schema.load(json_input)
            self.db.session.add(data)
            self.db.session.commit()
            return jsonify(success=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422

    def delete_request(self, id):
        """
        Preforms a delete request of the object with the primary key value of id
        :param id: id of object being deleted
        :return: Success status of request
        """
        model_id = escape(id)
        x = self.model.query.filter(getattr(self.model,self.id) == model_id).delete()
        if x == 0:
            abort(404)
        self.db.session.commit()
        resp = jsonify(success=True)
        return resp
