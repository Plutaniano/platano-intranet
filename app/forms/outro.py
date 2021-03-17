from flask_wtf import FlaskForm
from wtforms import TextField, DateField
from wtforms.fields.core import DecimalField
from wtforms.validators import DataRequired, Length


class OutroForm(FlaskForm):
    codigo_a = TextField('Código A (somente números)',
                         validators=[DataRequired()]
                        )

    descricao = TextField('Descrição',
                        validators=[DataRequired(),Length(min=1, max=120)]
                        )

    valor = DecimalField('Valor',
                        validators=[DataRequired()]
                        )                     

    mes_de_entrada = DateField('Ano/mês de Referência',
                                format='%Y-%m',
                                validators=[DataRequired()],
                                )
