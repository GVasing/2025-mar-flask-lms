from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp
from marshmallow import fields
from models.students import Student
from models.teachers import Teacher
from models.course import Course

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        load_instance = True
        include_fk = True
        include_relationships = True
        fields = ("id", "name", "department", "address", "courses")
        ordered = True

    courses = fields.List(fields.Nested("CourseSchema", exclude=("teacher", "id",)))

class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        include_fk = True
        include_relationships = True
        ordered = True
        fields = ("id", "name", "duration", "teacher")

    # name = fields.String(required=True, validate=And(
    #     Length(min=2, error="Course name must be at least two characters long"),  
    #     Regexp("[A-Za-z][A-Za-z0-9 ]*$", error="Only letters, numbers, and spaces are allowed.")
    # ))

    # duration = fields.Float(allow_nan=False, required=False)

    teacher = fields.Nested("TeacherSchema", only=("id", "name", "department"))


# Student Schema for converting a single entry
student_schema = StudentSchema()
# Student Schema for converting multiple entries
students_schema = StudentSchema(many=True)

# Student Schema for converting a single entry
teacher_schema = TeacherSchema()
# Student Schema for converting multiple entries
teachers_schema = TeacherSchema(many=True)

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)