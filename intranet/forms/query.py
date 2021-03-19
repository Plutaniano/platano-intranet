from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from .. import app
from intranet.models import db, Usuario, TABELAS_COM_RECEITA


class QueryForm(FlaskForm):
    ano_mes = SelectField('Ano/mês',
                          validators=[DataRequired()],
                          choices=[]
                          )

    id = SelectField('Usuários',
                             validators=[DataRequired()],
                             choices=list(db.session.query(Usuario.id, Usuario.nome))
                             )

    tabela = SelectField('Fonte',
                         validators=[DataRequired()],
                         choices=[
                             *((name, table.__displayname__) for name, table in TABELAS_COM_RECEITA.items())
                             ])
