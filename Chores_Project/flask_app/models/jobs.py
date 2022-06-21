from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users


class Job:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.accepted = data['accepted']
        self.user = None

    @classmethod 
    def save(cls, data):
        query = "INSERT INTO jobs (title, description, location, user_id) VALUES (%(title)s, %(description)s, %(location)s, %(user_id)s);"
        return connectToMySQL('chores_schema').query_db(query, data)


    @classmethod 
    def get_all(cls):
        query  = "SELECT * FROM jobs JOIN users ON users.id = jobs.user_id;"
        result = connectToMySQL('chores_schema').query_db(query)
        list_of_jobs = []
        for row in result:
            this_job = cls(row)
            users_dictionary = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            associated_user = users.User(users_dictionary)
            this_job.user = associated_user
            list_of_jobs.append(this_job)
        return list_of_jobs


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM jobs JOIN users ON users.id = jobs.user_id WHERE jobs.id = %(id)s;"
        result = connectToMySQL('chores_schema').query_db(query, data)
        this_job = cls(result[0])
        users_dictionary = {
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'password': result[0]['password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at'],
                'accepted': result[0]['accepted']
            }
        associated_user = users.User(users_dictionary)
        this_job.user = associated_user
        return this_job


    @staticmethod
    def validate_jobs(data):
        is_valid = True 
        if len(data['title']) < 3:
            flash('Title must be a minimum of 3 characters.')
            is_valid = False
        if len(data['description']) < 10:
            flash('Description must be a minimum of 10 characters.')
            is_valid = False
        if data['location'] == "":
            flash('Location field must be filled in.')
            is_valid = False
        return is_valid


    @classmethod 
    def update(cls, data):
        query = "UPDATE jobs SET title = %(title)s, description = %(description)s, location = %(location)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('chores_schema').query_db(query, data)


    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM jobs where id = %(id)s;"
        return connectToMySQL('chores_schema').query_db(query, data)


    @classmethod
    def accept(cls, data):
        query = "UPDATE jobs SET accepted = accepted +1 WHERE id = %(id)s;"
        return connectToMySQL('chores_schema').query_db(query, data)


    @classmethod
    def user_accept(cls, data):
        query = "INSERT INTO accepted (user_id, job_id, created_at, updated_at) VALUES (%(user_id)s, %(job_id)s, NOW(), NOW());"
        return connectToMySQL('chores_schema').query_db(query, data)


    @classmethod
    def get_all_accepted(cls, data):
        query = "SELECT * FROM jobs LEFT JOIN users ON users.id = jobs.user_id LEFT JOIN accepted on accepted.job_id = jobs.id WHERE accepted.user_id = %(id)s;"
        result = connectToMySQL('chores_schema').query_db(query, data)
        list_of_jobs = []
        for row in result:
            this_job = cls(row)
            users_dictionary = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            associated_user = users.User(users_dictionary)
            this_job.user = associated_user
            list_of_jobs.append(this_job)
        return list_of_jobs