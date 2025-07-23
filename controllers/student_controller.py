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
    data = students_schema.dump(students_list) # JSON Object

    if data:
        return jsonify(data)
    else:
        return {"message": "Not student records found"}, 404

# GET /id
# POST /
# PUT/PATCH /id
# DELETE /id