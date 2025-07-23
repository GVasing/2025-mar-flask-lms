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
@student_bp.route("/", methods=["POST"])
def create_a_student():
    # GET info from the request body
    body_data = request.get_json()
    # Create a Student Object from Student class/model with body response data
    new_student = Student(
        name=body_data.get("name"),
        email=body_data.get("email"),
        address=body_data.get("address")
    )
    # Add new student data to session
    db.session.add(new_student)
    # Commit the session
    db.session.commit()
    # Return
    return jsonify(student_schema.dump(new_student)), 201
# PUT/PATCH /id
# @student_bp.route("/<int:id>", methods=["PUT"])
# def edit_a_student():

# DELETE /id
# @student_bp.route("/<int:id>", methods=["DELETE"])
# def delete_a_student():
