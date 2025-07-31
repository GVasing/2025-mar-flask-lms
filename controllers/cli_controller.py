from flask import Blueprint
from init import db
from models.students import Student
from models.teachers import Teacher
from models.course import Course
from models.enrolment import Enrolment

# Define/Create a blueprint of 'app'
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_table():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Tables dropped.")

@db_commands.cli.command("seed")
def seed_tables():
    # Create an instance of the Model
    students = [
        Student(
            name="Alice",
            email="alice@email.com",
            address="Sydney"
        ), 
        Student(
            name="Bob",
            email="bob@email.com",
            address="Melbourne"
        )
    ]
    # Add to session
    db.session.add_all(students)

    teachers = [
        Teacher(
            name = "Teacher A",
            department = "Science",
            address = "Sydney"
        ),
        Teacher(
            name = "Teacher B",
            department = "Management",
            address = "Perth"
        )
    ]

    db.session.add_all(teachers)

    db.session.commit()

    courses = [
        Course(
            name = "Physics",
            duration = 3.5,
            teacher_id=teachers[0].id
        ), 
        Course(
            name = "Chemistry",
            duration = 4.0,
            teacher_id=teachers[1].id
        )
    ]

    db.session.add_all(courses)

    # Commit
    db.session.commit()
    print("Tables seeded.")