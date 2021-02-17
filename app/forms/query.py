from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired


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
                             ('investimentos', 'Investimentos'),
                             ('previdencia', 'Previdência'),
                             ('co_corretagem', 'Co-Corretagem'),
                             ('bancoXP', 'Banco XP'),
                             ('incentivo_previdencia', 'Incentivo Previdência'),
                             ('cambio', 'Câmbio')
                             ])
