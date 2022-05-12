from flask import Flask, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from config import Configuration
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


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAminView(AdminMixin, AdminIndexView):
    pass


class ArticleModelView(AdminMixin, BaseModelView):
    form_columns = ['title', 'subtitle', 'first_chapter', 'first_image', 'second_chapter', 'video',
                    'third_chapter', 'third_image', 'conclusion', 'themes']

class ThemeModelView(AdminMixin, BaseModelView):
    form_columns = ['name']


adm = Admin(app, 'HeavyReview', url='/', index_view=HomeAminView(name='Home'))

adm.add_view(ThemeModelView(Themes, db.session))
adm.add_view(ArticleModelView(Articles, db.session, name='Posts'))
adm.add_view(AdminView(User, db.session, name='Users'))
adm.add_view(AdminView(Commentaries, db.session, name='Commentaries'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
