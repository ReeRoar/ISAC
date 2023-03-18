from flask import jsonify
from markupsafe import escape
from generic_requests.GenericRequest import GenericRequest

class ManyToManyRequest(GenericRequest):
    def __init__(self, join_model, schema, join_schema, model1, model2, has_reqparse=True):
        self.model2 = model2
        self.join_model = join_model
        self.join_schema = join_schema
        self.model1 = model1
        super().__init__(join_model,schema, has_reqparse)

    def get_all_joined(self):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        query_result = self.db.session.query(self.model1, self.model2, self.join_model).filter(self.model1.id == self.join_model.model_id, self.model2.id == self.join_model.model2_id).all()
        return jsonify([self.join_schema.dump(obj) for obj in query_result])

    def get_all_joined_by_model_id(self,model1_id):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        model_id = escape(model1_id)
        query_result = self.db.session.query(self.model1, self.model2, self.join_model).filter(
            model_id == self.model1.id, self.model1.id == self.join_model.model_id,
            self.model2.id == self.join_model.model2_id).all()
        return jsonify([self.join_schema.dump(obj) for obj in query_result])

    def get_all_joined_by_model2_id(self,model2_id):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        model_id = escape(model2_id)
        query_result = self.db.session.query(self.model1, self.model2, self.join_model).filter(
            model_id == self.model2.id, self.model1.id == self.join_model.model_id,
            self.model2.id == self.join_model.model2_id).all()
        return jsonify([self.join_schema.dump(obj) for obj in query_result])