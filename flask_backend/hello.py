from flask import Flask, request, jsonify, abort
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import json
from flask_marshmallow import Marshmallow
from flask_restful import reqparse
from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
    post_dump,
    post_load,
    ValidationError,
)

db = SQLAlchemy()

app = Flask(__name__)
ma = Marshmallow(app)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:password@localhost/flask_test'

db.init_app(app)


@app.route('/<name>')
def hello_world(name):
    return f'<p> hello {escape(name)} </p>'


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(32))


class ModelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Model
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    @post_load
    def make_model(self,data,**kwargs):
        return Model(**data)

with app.app_context():
    db.create_all()


@app.route('/models', methods=['GET', 'POST'])
def models():
    model_schema = ModelSchema()
    if request.method == 'GET':
        query_result = Model.query.all()
        return jsonify([model_schema.dump(obj) for obj in query_result])
    if request.method == 'POST':
        json_input = request.json
        try:
            data = model_schema.load(json_input)
            db.session.add(data)
            db.session.commit()
            return jsonify(success=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422


@app.route('/models/<model_id>', methods=['GET', 'DELETE','PUT'])
def models_id(model_id):
    model_schema = ModelSchema()
    if request.method == 'GET':
        model_id = escape(model_id)
        model = Model.query.get_or_404(model_id)
        return jsonify(model_schema.dump(model))
    if request.method == 'PUT':
        json_input = request.json
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, location='json')
            parser.add_argument('email', type=str, location='json')
            parser.add_argument('id', type=int, location='json')
            model = Model.query.get_or_404(model_id)
            args = parser.parse_args()
            for key, value in args.items():
                if args[key] is not None:
                    setattr(model, key, value)
            db.session.commit()
            return jsonify(success=True)
        except ValidationError as err:
            return {"errors": err.messages}, 422
    if request.method == 'DELETE':
        x = Model.query.filter_by(id=model_id).delete()
        if x == 0:
            abort(404)
        db.session.commit()
        resp = jsonify(success=True)
        return resp


if __name__ == '__main__':
    app.run(debug=True)
