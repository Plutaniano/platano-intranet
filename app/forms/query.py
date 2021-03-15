from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from .. import app


class QueryForm(FlaskForm):
    ano_mes = SelectField('Ano/mês',
                          validators=[DataRequired()],
                          choices=[]
                          )

    assessores = SelectField('Assessor',
                             validators=[DataRequired()],
                             choices=[]
                             )

    tabela = SelectField('Fonte',
                         validators=[DataRequired()],
                         choices=[
                             *((name, table.__displayname__) for name, table in app.config['TABELAS_COM_RECEITA'].items())
                             ])
