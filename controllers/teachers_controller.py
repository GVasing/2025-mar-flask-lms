from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from init import db
from models.teachers import Teacher, teacher_schema, teachers_schema
from psycopg2 import errorcodes