from flask_restful import reqparse
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from app import db, ma


class Student(db.Model):
    student_id: Mapped[BigInteger] = db.Column(db.BigInteger, primary_key=True)
    first_name: Mapped[str] = db.Column(db.String(32), nullable=False)
    last_name: Mapped[str] = db.Column(db.String(32), nullable=False)
    email: Mapped[str] = db.Column(db.String(32))
    sign_in = db.relationship('SignIn', backref='student', lazy=True)
    student_enrollment = db.relationship('StudentEnrollment', backref='student', lazy=True)
    attendance = db.relationship('Attendance', backref='student', lazy=True)


class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student

    student_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String()

    @post_load
    def make_model(self, data, **kwargs):
        return Student(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        return parser
