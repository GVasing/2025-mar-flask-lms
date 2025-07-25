from flask import Flask
from controllers.cli_controller import db_commands
from controllers.student_controller import student_bp
from controllers.teachers_controller import teacher_bp
from init import db
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Initialise SQL Database
    db.init_app(app)

    # Register Blueprint
    app.register_blueprint(db_commands)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)

    return app 