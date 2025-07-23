from flask import Blueprint, jsonify, request
from init import db
from models.students import Student, student_schema, students_schema


student_bp = Blueprint("student", __name__, url_prefix="/students")

# Routes
# GET /
@student_bp.route("/")
def get_students():
    # Define GET statement
    stmt = db.select(Student)
    # Execute it
    students_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = students_schema.dump(students_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "Not student records found"}, 404

# GET /id
@student_bp.route("/<int:student_id>")
def get_a_student(student_id):
    # Define GET statment
    stmt = db.select(Student).where(Student.id == student_id)

    # Execute it
    student = db.session.scalar(stmt)

    # Error Handling
    if student:
        # Serialise
        data = student_schema.dump(student)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Student with id {student_id} not found."}, 404
# POST /
# PUT/PATCH /id
# DELETE /id