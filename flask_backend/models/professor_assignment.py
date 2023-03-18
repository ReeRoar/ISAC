from flask_restful import reqparse
from marshmallow import (
    fields,
    post_load,
)
from sqlalchemy.orm import Mapped
from sqlalchemy import DateTime
from app import db, ma
from models.course import Course, CourseSchema
from models.professor import Professor, ProfessorSchema


class ProfessorAssignment(db.Model):
    """
    model_id = professor id
    model2_id = course id
    """
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    model2_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("professor.id"), nullable=False)



class ProfessorAssignmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ProfessorAssignment

    id = fields.Integer()
    model2_id = fields.Integer()
    model_id = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
        return ProfessorAssignment(**data)

    def get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('model2_id', type=DateTime, location='json')
        parser.add_argument('model_id', type=int, location='json')
        return parser


class ProfessorAssignmentJoinedSchema(ma.SQLAlchemySchema):
    class Meta:
        course = Course
        professor = Professor
        ProfessorAssignment = ProfessorAssignment

    Course = fields.Nested(CourseSchema)
    Professor = fields.Nested(ProfessorSchema)
    ProfessorAssignment = fields.Nested(ProfessorAssignmentSchema)