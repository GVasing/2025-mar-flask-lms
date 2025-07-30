from init import db

class Teacher (db.Model):
    # Name table
    __tablename__ = "teachers"
    # Define primary key attribute
    id = db.Column(db.Integer, primary_key=True)
    # Define non key attributes
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(150))

    courses = db.relationship("Course", back_populates="teacher")