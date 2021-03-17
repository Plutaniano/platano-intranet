from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, Length, Email


class ForgotForm(FlaskForm):
    codigo_a = TextField('Email',
                                validators=[DataRequired(),
                                            Length(min=6, max=40),
                                            Email()])
