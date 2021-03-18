from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, Email, NumberRange, Length


class RegisterForm(FlaskForm):
    codigo_a = TextField('Código A (somente números)',
                                validators=[
                                    DataRequired(),
                                    Length(min=5, max=5)
                                    ])

    name = TextField('Nome',
                     validators=[
                         DataRequired(),
                         Length(min=6, max=60)
                         ])

    email = TextField('Email',
                      validators=[
                          DataRequired(),
                          NumberRange(10000, 99999),
                          Email()])
