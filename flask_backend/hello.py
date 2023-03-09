from flask import Flask, request, jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import json
from flask_marshmallow import Marshmallow

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

with app.app_context():
    db.create_all()


@app.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'GET':
        model_schema = ModelSchema()
        query_result = Model.query.all()
        return jsonify([model_schema.dump(obj) for obj in query_result])

    if request.method == 'POST':
        content = request.json
        model1 = Model(id=content['id'], username=content["username"], email=content["email"])
        db.session.add(model1)
        db.session.commit()
        resp = jsonify(success=True)
        return resp


@app.route('/models/<model_id>', methods=['GET', 'DELETE','PUT'])
def models_id(model_id):
    if request.method == 'GET':
        model_id = escape(model_id)
        model_schema = ModelSchema()
        query_result = Model.query.filter_by(id=model_id).one()
        return jsonify(model_schema.dump(query_result))

    if request.method == 'PUT':
        content = request.json
        model = Model.query.filter_by(id=model_id).first()
        model.id = content['id']
        model.username = content['username']
        model.email = content['email']
        db.session.commit()
        resp = jsonify(success=True)
        return resp

    if request.method == 'DELETE':
        Model.query.filter_by(id=model_id).delete()
        db.session.commit()
        resp = jsonify(success=True)
        return resp

if __name__ == '__main__':
    app.run(debug=True)
