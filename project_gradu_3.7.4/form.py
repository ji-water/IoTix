from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField

class LoginForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    user_pw = PasswordField('user_pw', validators=[DataRequired()])