
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users import User
from flask_app.models.jobs import Job
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login_user():
    data = {'email': request.form['email']}
    user_in_db = User.validate_user(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/jobs')


@app.route('/register', methods=['POST'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/')


@app.route('/logout') 
def logout_user():
    session.clear()
    return redirect('/')

