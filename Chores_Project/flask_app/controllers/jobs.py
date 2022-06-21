
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users import User
from flask_app.models.jobs import Job


@app.route('/jobs')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': session['user_id']}
    return render_template('dashboard.html', users=User.get_by_id(data), jobs=Job.get_all(), accepted_jobs=Job.get_all_accepted(data))


@app.route('/jobs/new')
def new_job():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': session['user_id']}
    return render_template('new_job.html', users=User.get_by_id(data))

@app.route('/create', methods=['POST'])
def create_job():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Job.validate_jobs(request.form):
        return redirect('/jobs/new') 
    data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'location': request.form['location'],
            'user_id': session['user_id']
    }
    Job.save(data)
    return redirect('/jobs')


@app.route('/jobs/<int:id>/edit')
def edit_jobs(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    session_data = {'id': session['user_id']}
    return render_template('edit_job.html', jobs=Job.get_one(data), users=User.get_by_id(session_data))

@app.route('/update/<int:id>', methods=['POST'])
def update_jobs(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Job.validate_jobs(request.form):
        return redirect(f'/jobs/{id}/edit')
    data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'location': request.form['location'],
            'id': id 
    }
    Job.update(data)
    return redirect('/jobs')


@app.route('/delete/<int:id>')
def delete_job(id):
    data = {'id': id}
    Job.delete(data)
    return redirect('/jobs')


@app.route('/jobs/<int:id>')
def show_job(id): 
    if 'user_id' not in session:
        return redirect('/logout')
    data = {'id': id}
    session_data = {'id': session['user_id']}
    return render_template('show_job.html', jobs=Job.get_one(data), users=User.get_by_id(session_data))


@app.route('/accept/<int:id>', methods=['POST'])
def accept(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'user_id': session['user_id'],
        'job_id': id,
        }
    data = {'id': id}
    Job.accept(data)
    Job.user_accept(user_data)
    return redirect('/jobs')

