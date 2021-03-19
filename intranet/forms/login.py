from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
