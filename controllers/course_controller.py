from flask import Blueprint, jsonify, request

from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.course import Course
from schemas.schemas import course_schema, courses_schema

course_bp = Blueprint("course", __name__, url_prefix="/courses" )

# Routes
# GET /
@course_bp.route("/")
def get_courses():
    # Define GET statement
    stmt = db.select(Course).order_by(Course.id)
    # Execute it
    courses_list = db.session.scalars(stmt) # Python Object
    # Serialise
    data = courses_schema.dump(courses_list) # JSON Object
    # Error Handling and Return
    if data:
        return jsonify(data)
    else:
        return {"message": "Not course records found"}, 404

# GET /id
@course_bp.route("/<int:course_id>")
def get_a_course(course_id):
    # Define GET statment
    stmt = db.select(Course).where(Course.id == course_id)

    # Execute it
    course = db.session.scalar(stmt)

    # Error Handling
    if course:
        # Serialise
        data = course_schema.dump(course)
        # Return data
        return jsonify(data)
    else:
        return {"message":f"Course with id {course_id} not found."}, 404
# POST /
@course_bp.route("/", methods=["POST"])
def create_a_course():
    try:
        # GET info from the request body
        body_data = request.get_json()
        # Create a Course Object from Course class/model with body response data
        new_course = Course(
            name=body_data.get("name"),
            duration=body_data.get("duration"),
            teacher_id = body_data.get("teacher_id")
        )
        # Add new course data to session
        db.session.add(new_course)
        # Commit the session
        db.session.commit()
        # Return
        return jsonify(course_schema.dump(new_course)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message":f"Required field {err.orig.diag.column_name} cannot be null"}, 400
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Course Name must be unique"}, 400
        
        else:
            return {"message": "Unexpected Error Occured"}, 400
# PUT/PATCH /id
@course_bp.route("/<int:course_id>", methods=["PUT", "PATCH"])
def update_course(course_id):
    try:
        # Define GET Statement
        stmt = db.select(Course).where(Course.id == course_id)

        # Execute statement
        course = db.session.scalar(stmt)

        # If/Elif/Else Conditions
        if course:
            # Retrieve 'course' data
            body_data = request.get_json()
            # Specify changes
            course.name = body_data.get("name") or course.name
            course.duration = body_data.get("duration") or course.duration
            course.teacher_id = body_data.get("teacher_id") or course.teacher_id
            # Commit changes
            db.session.commit()
            # Return data
            return jsonify(course_schema.dump(course))
        else:
            return {"message": f"Course with id {course_id} does not exist/cannot be found."}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Course Name must be unique"}, 400
        
        else:
            return {"message": "Unexpected Error Occured"}, 400
    except DataError as err:
    #     # if err.orig.
        return {"message" : err.orig.diag.message_primary}, 400

# DELETE /id
@course_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_a_course(course_id):
        # Find the course with the course_id
    stmt = db.select(Course).where(Course.id == course_id)
    course = db.session.scalar(stmt)
    # if exists
    if course:
        # delete the course entry
        db.session.delete(course)
        db.session.commit()

        return {"message": f"Course '{course.name}' has been removed successfully."}, 200
    # else:
    else:
        # return an acknowledgement message
        return {"message": f"Course with id '{course_id}' does not exist"}, 404