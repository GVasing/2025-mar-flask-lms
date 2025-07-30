from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from init import db
from models.teachers import Teacher
from psycopg2 import errorcodes
from schemas.schemas import teacher_schema, teachers_schema

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teachers")

# Routes
# GET /
@teacher_bp.route("/")
def get_teachers():
    department = request.args.get("department")
    if department:
        stmt = db.select(Teacher).where(Teacher.department == department).order_by(Teacher.id)
    else:
    # Define GET statement
        stmt = db.select(Teacher).order_by(Teacher.id)
    # Execute it
    teachers_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = teachers_schema.dump(teachers_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "Not teacher records found"}, 404

# GET /id
@teacher_bp.route("/<int:teacher_id>")
def get_a_teacher(teacher_id):
    # Define GET statment
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)

    # Execute it
    teacher = db.session.scalar(stmt)

    # Error Handling
    if teacher:
        # Serialise
        data = teacher_schema.dump(teacher)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Teacher with id {teacher_id} not found."}, 404
# POST /
@teacher_bp.route("/", methods=["POST"])
def create_a_teacher():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Teacher Object from Teacher class/model with body response data
        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address")
        )
        # Add new teacher data to session
        db.session.add(new_teacher)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(teacher_schema.dump(new_teacher)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        # if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
        #     return {"message": "Email must be unique"}, 400
        
        # else:
        #     return {"message": "Unexpected Error Occured"}, 400
# PUT/PATCH /id
@teacher_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    # Define GET Statement
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)

    # Execute statement
    teacher = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if teacher:
        # Retrieve 'teacher' data
        body_data = request.get_json()
        # Specify changes
        teacher.name = body_data.get("name") or teacher.name
        teacher.department = body_data.get("department") or teacher.department
        teacher.address = body_data.get("address") or teacher.address
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(teacher_schema.dump(teacher))
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist/cannot be found."}, 404

# DELETE /id
@teacher_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_a_teacher(teacher_id):
        # Find the teacher with the teacher_id
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)
    # if exists
    if teacher:
        # delete the teacher entry
        db.session.delete(teacher)
        db.session.commit()

        return {"message": f"Teacher '{teacher.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Teacher with id '{teacher_id}' does not exist"}, 404