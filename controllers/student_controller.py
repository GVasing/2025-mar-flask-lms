from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from init import db
from models.students import Student, student_schema, students_schema
from psycopg2 import errorcodes


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
    try:
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
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Email must be unique"}, 400
        
        else:
            return {"message": "Unexpected Error Occured"}, 400
# PUT/PATCH /id
@student_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_student(student_id):
    # Define GET Statement
    stmt = db.select(Student).where(Student.id == student_id)

    # Execute statement
    student = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if student:
        # Retrieve 'student' data
        body_data = request.get_json()
        # Specify changes
        student.name = body_data.get("name") or student.name
        student.email = body_data.get("email") or student.email
        student.address = body_data.get("address") or student.address
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(student_schema.dump(student))
    else:
        return {"message": f"Student with id {student_id} does not exist/cannot be found."}, 404

# DELETE /id
@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_a_student(student_id):
        # Find the student with the student_id
    stmt = db.select(Student).where(Student.id == student_id)
    student = db.session.scalar(stmt)
    # if exists
    if student:
        # delete the student entry
        db.session.delete(student)
        db.session.commit()

        return {"message": f"Student '{student.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Student with id '{student_id}' does not exist"}, 404