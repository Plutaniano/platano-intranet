from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange
import email_validator

class RegisterForm(FlaskForm):
    codigo_assessor = TextField('Código A (somente números)', validators=[DataRequired(), Length(min=5, max=5)])
    name = TextField('Nome',                     validators=[DataRequired(), Length(min=6, max=60)])
    email = TextField('Email',                   validators=[DataRequired(), NumberRange(10000, 99999), Email()])


class LoginForm(FlaskForm):
    codigo_assessor = TextField('Código A',      validators=[DataRequired()])
    password = PasswordField('Senha',            validators=[DataRequired()])


class ForgotForm(FlaskForm):
    codigo_assessor = TextField('Email',         validators=[DataRequired(), Length(min=6, max=40), Email()])


class QueryForm(FlaskForm):
    ano_mes = SelectField('Ano/mês',             validators=[DataRequired()], choices=[])
    assessores = SelectField('Assessor',         validators=[DataRequired()], choices=[])
    tabela = SelectField('Fonte',                validators=[DataRequired()], choices=[('investimentos', 'Investimentos'),
                                                                                       ('previdencia', 'Previdência'),
                                                                                       ('co_corretagem', 'Co-Corretagem'),
                                                                                       ('bancoXP','Banco XP'),
                                                                                       ('incentivo_previdencia', 'Incentivo Previdência'),
                                                                                       ('cambio', 'Câmbio')
                                                                                       ])
