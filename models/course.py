from init import db
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Intger, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    duration = db.Column(db.float)

    # one-to-many with teacher
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

    teacher = db.relationship("Teacher", back_populate="courses")

class CourseSchema(db.Schema):
    name = fields.String(required=True, validate=And(
        Length(min=2, error="Course name must be at least two characters long"),  
        Regexp("[A-Za-z][A-Za-z0-9 ]*$", error="Only letters, numbers, and spaces are allowed.")
    ))

    duration = fields.Float(allow_nan=False, required=False)

    teacher = fields.Nested("TeacherSchema", only=["name", "department"])

    class Meta:
        fields = ("id", "name", "duration")

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)