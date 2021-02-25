from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


class ResumoForm(FlaskForm):
    ano_mes = SelectField('Ano/mês',
                          validators=[DataRequired()],
                          choices=[]
                          )

    assessores = SelectField('Assessor',
                             validators=[DataRequired()],
                             choices=[]
                             )