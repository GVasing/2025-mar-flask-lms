# Creating an LMS app with entities
- Student
- Teacher
- Courses
- Enrollments (Junction Table)

To run the server succesfully, here are the steps you need to perform:
- create a .env file witht the variables included in .env.example
    - DATABASE_URI with a connection string to your chosen database e.g. postgres

- ensure that a local database exists by making one in the postgres shell
    - enter the postgres shell
        - MacOS: run the `psql` command
        - Linux & WSL: run the `sudo -u postgres psql` command 
    - list all existing databases by running `\l`
    - if the database you want to use does not currently exist, create it by running `CREATE DATABASE lms_db;`
    - check that it exists by running `\l` again
    - connect to the database you want to use with `\c lms_db`
- ensure that a postgres shell user that has permissions to work with your database 
    - in the postgres shell, run `CREATE USER lms_dev WITH PASSWORD '123456';`
    - grant the user the permissions needed to work with the database, run `GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_dev;`
    - grant db schema permissions to the user as well, run `GRANT ALL ON SCHEMA public TO lms_dev;`
- exit the postgres shell with `\q`

- Create a virtual environment
    - Run command in terminal: 'python3 -m venv venv'
- Activate virtual environment:
    - WSL & Linux & MacOs: 'source venv/bin/activate'
    - Windows: 'venv/Scripts/activate'
- Set the VSCode Python interperter to the venv Python binary:
    - CTRL + Shift + P to open up the command palette
    - Choose the interpreter with the path that matches the "venv" path.
- Intsall dependencies from the from the project within the activated virtual environment
    - Run command in terminal: 'pip install -r ./requirements.txt'

- Create a .flaskenv file and define: 
    - FLASK_APP=main
    (Extra Optional Code.)
    - FLASK_DEBUG=True or FLASK_DEBUG=1
    - FLASK_RUN_PORT=8080

- Ensure that the flask app database exists and has any seed datat that it's meant to have
    - Check the source code for any CLI commands, e.g. './controllers/cli_controller.py'
    - Run the commands needed to drop tables, create tables, and then seed those created tables.

- Flask run to run the server.

## API Endpoints

Endpoint                      Methods     Rule                          
----------------------------  ----------  ------------------------------
course.create_a_course        POST        /courses/                     
course.delete_a_course        DELETE      /courses/<int:course_id>      
course.get_a_course           GET         /courses/<int:course_id>      
course.get_courses            GET         /courses/                     
course.update_course          PATCH, PUT  /courses/<int:course_id>      
enrolment.create_a_enrolment  POST        /enrolments/                  
enrolment.delete_a_enrolment  DELETE      /enrolments/<int:id>          
enrolment.get_a_enrolment     GET         /enrolments/<int:enrolment_id>
enrolment.get_enrolments      GET         /enrolments/                  
enrolment.update_enrolment    PATCH, PUT  /enrolments/<int:id>          
student.create_a_student      POST        /students/                    
student.delete_a_student      DELETE      /students/<int:id>            
student.get_a_student         GET         /students/<int:student_id>    
student.get_students          GET         /students/                    
student.update_student        PATCH, PUT  /students/<int:id>            
teacher.create_a_teacher      POST        /teachers/                    
teacher.delete_a_teacher      DELETE      /teachers/<int:teacher_id>    
teacher.get_a_teacher         GET         /teachers/<int:teacher_id>    
teacher.get_teachers          GET         /teachers/                    
teacher.update_teacher        PATCH, PUT  /teachers/<int:teacher_id>    