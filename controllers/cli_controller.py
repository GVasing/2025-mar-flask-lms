from flask import Blueprint
from init import db
from models.students import Student

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
    # Commit
    db.session.commit()
    print("Tables seeded.")