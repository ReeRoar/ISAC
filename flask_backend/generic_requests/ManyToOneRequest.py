from flask import jsonify
from markupsafe import escape
from generic_requests.GenericRequest import  GenericRequest

class ManyToOneRequest(GenericRequest):
    def __init__(self, many_model, schema, db, one_model, joined_schema, has_reqparse=False):
        super().__init__(many_model, schema, db, has_reqparse)

        self.one_model = one_model
        self.joined_schema = joined_schema

    def get_all_joined(self):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        query_result = self.db.session.query(self.model, self.one_model).filter(
            self.one_model.id == self.model.model_id).all()
        return jsonify([self.joined_schema.dump(obj) for obj in query_result])

    def get_all_joined_by_one_model_id(self, id):
        one_model_id = escape(id)
        query_result = self.db.session.query(self.model, self.one_model).filter(
            self.one_model.id == self.model.model_id).filter(self.one_model.id == one_model_id).all()
        return jsonify([self.joined_schema.dump(obj) for obj in query_result])