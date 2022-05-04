from flask import Flask, redirect, url_for, request, session
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from datetime import datetime
from datetime import timedelta



app = Flask(__name__)
app.config.from_object(Configuration)


db = SQLAlchemy(app)
migtate = Migrate(app, db)


from models import *
adm = Admin(app, 'HeavyReview', url='/', index_view=AdminIndexView(name='Home'))

adm.add_view(ModelView(Themes, db.session))
adm.add_view(ModelView(Articles, db.session, name='Posts'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
