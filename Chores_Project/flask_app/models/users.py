
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import jobs
import re	
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.jobs = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('chores_schema').query_db(query, data)


    @classmethod
    def validate_user(cls, data): 
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('chores_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_register(data):
        is_valid = True 
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('chores_schema').query_db(query, data)
        if len(result) >= 1:
            flash('Email is already taken')
        if not EMAIL_REGEX.match(data['email']): 
            flash('Invalid Email')
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match')
            is_valid = False
        return is_valid


    @classmethod
    def get_user(cls, data): 
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('chores_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_by_id(cls, data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('chores_schema').query_db(query, data)
        return cls(result[0])

