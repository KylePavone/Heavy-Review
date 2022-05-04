from wtforms import Form, StringField, TextAreaField
from wtforms.validators import InputRequired

class CommentForm(Form):
    commentary = TextAreaField('content', [InputRequired()])

