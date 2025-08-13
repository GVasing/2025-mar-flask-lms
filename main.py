# Built-In imports
import os

# Installed imports
from flask import Flask
from dotenv import load_dotenv

# Created module imports
from controllers.cli_controller import db_commands
from controllers.student_controller import student_bp
from controllers.teachers_controller import teacher_bp
from controllers.course_controller import course_bp
from controllers.enrolment_controller import enrolment_bp
from init import db
from utils.error_handlers import register_error_handlers

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Initialise SQL Database
    db.init_app(app)
    
    # Specify auto sort of keys/attributes to be disabled when GET is requested
    app.json.sort_keys = False

    # Register Blueprint
    app.register_blueprint(db_commands)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrolment_bp)
    register_error_handlers(app)

    return app 