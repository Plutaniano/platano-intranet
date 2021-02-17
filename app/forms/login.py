from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    codigo_a = TextField('Código A', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
