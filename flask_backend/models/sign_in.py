from flask_restful import reqparse, inputs
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime
from app import db, ma, login_manager
from models import student


class SignIn(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    time: Mapped[DateTime] = db.Column(db.DateTime, server_default=db.func.now())
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)


class SignInSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SignIn

    id = fields.Integer()
    time = fields.DateTime()
    student_id = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
        return SignIn(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('time', type=inputs.datetime_from_iso8601, location='json')
        parser.add_argument('student_id', type=int, location='json')
        return parser


class StudentSignInSchema(ma.SQLAlchemySchema):
    class Meta:
        student = student.Student
        sign_in = SignInSchema

    Student = fields.Nested(student.StudentSchema)
    SignIn = fields.Nested(SignInSchema)
