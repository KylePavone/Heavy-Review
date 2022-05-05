from app import app, db, user_datastore
from flask import render_template, request, redirect, session, url_for
from forms import RegisterForm, ChangepPassForm
from datetime import timedelta
from models import User, Role


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=5)


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('about.html')

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


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangepPassForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User.query.filter(User.email == form.email.data).first()
                user.password = form.new_password.data
                db.session.commit()
            except:
                return "Wrong email!"
        return redirect(url_for('security.login'))
    return render_template('forgot_password.html', form=form)




