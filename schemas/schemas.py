from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.validate import Length, And, Regexp
from marshmallow import validates, ValidationError, fields
from models.students import Student
from models.teachers import Teacher
from models.course import Course
from models.enrolment import Enrolment

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        include_relationships = True
        fields = ("id", "name", "email", "address", "enrolments")
        ordered = True

    enrolments = fields.List(fields.Nested("EnrolmentSchema", only=("id", "enrolment_date", "course")))

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
        fields = ("id", "name", "duration", "teacher", "enrolments")

    # @validates("property-to-validate")
    # def some_function_name(self, property-to-validate, data_key)
    @validates("name")
    def validates_name(self, name, data_key):
        if len(name) < 2:
            print("Course name is too short")
            raise ValidationError("Course name is too short")
        

    # name = fields.String(required=True, validate=And(
    #     Length(min=2, error="Course name must be at least two characters long"),  
    #     Regexp("[A-Za-z][A-Za-z0-9 ]*$", error="Only letters, numbers, and spaces are allowed.")
    # ))

    # duration = fields.Float(allow_nan=False, required=False)

    teacher = fields.Nested("TeacherSchema", only=("id", "name", "department"))
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=("course",)))

class EnrolmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Enrolment
        load_instance = True
        include_relationships = True
        include_fk = True
        ordered = True
        fields = ("id", "enrolment_date", "student_id", "course_id", "student", "course")

    student = fields.Nested("StudentSchema", only=("id", "name"))
    course = fields.Nested("CourseSchema", only=("id", "name"))

# Student Schema for converting a single entry
student_schema = StudentSchema()
# Student Schema for converting multiple entries
students_schema = StudentSchema(many=True)

# Teacher Schema for converting a single entry
teacher_schema = TeacherSchema()
# Teacher Schema for converting multiple entries
teachers_schema = TeacherSchema(many=True)

# Course Schema for converting a single entry
course_schema = CourseSchema()
# Course Schema for converting a multiple entry
courses_schema = CourseSchema(many=True)

# Enrolment Schema for converting a single entry
enrolment_schema = EnrolmentSchema()
# Enrolment Schema for converting a multiple entry
enrolments_schema = EnrolmentSchema(many=True)