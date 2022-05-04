from app import app, db, user_datastore
from flask import render_template, request, redirect, session
from forms import RegisterForm
from datetime import timedelta
from models import User, Role


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=5)


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = user_datastore.create_user(name=form.name.data, email=form.email.data, password=form.password.data)
            role = Role.query.filter(Role.name == 'user').first()
            user_datastore.add_role_to_user(new_user, role)
            db.session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)
