from flask_wtf import FlaskForm
from wtforms import TextField, DateField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length

from intranet.models import db, Usuario


class OutroForm(FlaskForm):
    usuario = SelectField('Usuarios', choices=db.session.query(Usuario.id, Usuario.nome))

    descricao = TextField('Descrição',
                        validators=[DataRequired(),Length(min=1, max=120)]
                        )

    valor = DecimalField('Valor',
                        validators=[DataRequired()]
                        )                     

    mes_de_entrada =DateField('Ano/mês de Referência',
                                format='%Y-%m',
                                validators=[DataRequired()],
                                )
