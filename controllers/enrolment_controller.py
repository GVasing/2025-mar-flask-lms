from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from init import db
from models.enrolment import Enrolment
from psycopg2 import errorcodes
from schemas.schemas import enrolment_schema, enrolments_schema


enrolment_bp = Blueprint("enrolment", __name__, url_prefix="/enrolments")

# Routes
# GET /
@enrolment_bp.route("/")
def get_enrolments():
    course_id = request.args.get("course_id", type=int)
    student_id = request.args.get("student_id", type=int)

    stmt = db.select(Enrolment)
    
    # Define GET statement
    if course_id:
        stmt = stmt.where(Enrolment.course_id == course_id)
    if student_id:
        stmt = stmt.where(Enrolment.student_id == student_id)

    # Execute it
    enrolments_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = enrolments_schema.dump(enrolments_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "Not enrolment records found"}, 404

# GET /id
@enrolment_bp.route("/<int:enrolment_id>")
def get_a_enrolment(enrolment_id):
    # Define GET statment
    stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)

    # Execute it
    enrolment = db.session.scalar(stmt)

    # Error Handling
    if enrolment:
        # Serialise
        data = enrolment_schema.dump(enrolment)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Enrolment with id {enrolment_id} not found."}, 404
# POST /
@enrolment_bp.route("/", methods=["POST"])
def create_a_enrolment():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Enrolment Object from Enrolment class/model with body response data
        new_enrolment = Enrolment(
            enrolment_date=body_data.get("enrolment_date"),
            student_id = body_data.get("student_id"),
            course_id = body_data.get("course_id")
        )
        # Add new enrolment data to session
        db.session.add(new_enrolment)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(enrolment_schema.dump(new_enrolment)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 400
        
        else:
            return {"message": "Unexpected Error Occured"}, 400
# # PUT/PATCH /id
@enrolment_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_enrolment(enrolment_id):
    # Define GET Statement
    stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)

    # Execute statement
    enrolment = db.session.scalar(stmt)

    # If/Elif/Else Conditions
    if enrolment:
        # Retrieve 'enrolment' data
        body_data = request.get_json()
        # Specify changes
        enrolment.name = body_data.get("name") or enrolment.name
        enrolment.email = body_data.get("email") or enrolment.email
        enrolment.address = body_data.get("address") or enrolment.address
        # Commit changes
        db.session.commit()
        # Return data
        return jsonify(enrolment_schema.dump(enrolment))
    else:
        return {"message": f"Enrolment with id {enrolment_id} does not exist/cannot be found."}, 404

# # DELETE /id
@enrolment_bp.route("/<int:id>", methods=["DELETE"])
def delete_a_enrolment(enrolment_id):
    # Find the enrolment with the enrolment_id
    stmt = db.select(Enrolment).where(Enrolment.id == enrolment_id)
    enrolment = db.session.scalar(stmt)
    # if exists
    if enrolment:
        # delete the enrolment entry
        db.session.delete(enrolment)
        db.session.commit()

        return {"message": f"Enrolment '{enrolment.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Enrolment with id '{enrolment_id}' does not exist"}, 404