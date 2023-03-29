from flask import jsonify
from markupsafe import escape
from generic_requests.GenericRequest import GenericRequest


class ManyToOneRequest(GenericRequest):
    def __init__(self, model, schema, one_model, joined_schema, one_model_id='id', id='id', has_reqparse=True):
        super().__init__(model, schema, id, has_reqparse)
        self.one_model_id = one_model_id
        self.one_model = one_model
        self.joined_schema = joined_schema

    def get_all_joined(self):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        query_result = self.db.session.query(self.model, self.one_model).filter(
            getattr(self.one_model,self.one_model_id) == getattr(self.model, self.one_model_id)).all()
        return jsonify([self.joined_schema.dump(obj) for obj in query_result])

    def get_all_joined_by_one_model_id(self, id):
        one_model_id = escape(id)
        query_result = self.db.session.query(self.model, self.one_model).filter(
            getattr(self.one_model, self.one_model_id) == getattr(self.model, self.one_model_id),
            getattr(self.one_model, self.one_model_id) == one_model_id).all()
        return jsonify([self.joined_schema.dump(obj) for obj in query_result])
