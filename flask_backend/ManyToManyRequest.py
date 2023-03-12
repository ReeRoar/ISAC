from flask import jsonify
from markupsafe import escape

from GenericRequest import GenericRequest

class ManyToManyRequest(GenericRequest):
    def __init__(self, model1, schema1,model2, schema2, join_model, join_schema, db, has_reqparse=False):
        self.model2 = model2
        self.schema2 = schema2
        self.join_model = join_model
        self.join_schema = join_schema
        super().__init__(model1,schema1,db,has_reqparse)

    def get_all_joined(self):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        query_result = self.db.session.query(self.model, self.model2, self.join_model).filter(self.model.id == self.join_model.model_id, self.model2.id == self.join_model.model2_id).all()
        print(query_result)
        #print(self.join_schema.dump(query_result[0]))
        return jsonify([self.join_schema.dump(obj) for obj in query_result])

    def get_all_joined_by_model_id(self,model1_id):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        model_id = escape(model1_id)
        query_result = self.db.session.query(self.model, self.model2, self.join_model).filter(
            self.model.id == self.join_model.model_id, self.model2.id == self.join_model.model2_id,
            model_id == self.model.id).all()
        print(query_result)
        #print(self.join_schema.dump(query_result[0]))
        return jsonify([self.join_schema.dump(obj) for obj in query_result])

    def get_all_joined_by_model2_id(self,model2_id):
        """
        Gets all joined rows of model
        :return: list of JSON objects containing each row of the model within the database. Each object is a nested JSON,
         containing the name of the object then each attribute
        """
        model_id = escape(model2_id)
        query_result = self.db.session.query(self.model, self.model2, self.join_model).filter(
            self.model.id == self.join_model.model_id, self.model2.id == self.join_model.model2_id,
            model_id == self.model2.id).all()
        print(query_result)
        #print(self.join_schema.dump(query_result[0]))
        return jsonify([self.join_schema.dump(obj) for obj in query_result])