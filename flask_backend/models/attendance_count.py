from flask_restful import reqparse, inputs
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime, Date, Boolean
from app import db, ma


class AttendanceCount(db.Model):
    """
    model id = course
    model id 2 = student
    """
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    camera_value: Mapped[int] = db.Column(db.Integer)
    rfid_value: Mapped[int] = db.Column(db.Integer)
    mismatch_counter: Mapped[int] = db.Column(db.Integer)


class AttendanceCountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AttendanceCount

    id = fields.Integer()
    camera_value = fields.Integer()
    rfid_value = fields.Integer()
    mismatch_counter = fields.Integer()


    @post_load
    def make_model(self, data, **kwargs):
        return AttendanceCount(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('camera_value', type=int, location='json')
        parser.add_argument('rfid_value', type=int, location='json')
        parser.add_argument('mismatch_counter', type=int, location='json')
        return parser
