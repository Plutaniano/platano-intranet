from flask_wtf import FlaskForm
from wtforms import DateField, FileField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    mes_de_entrada = DateField('Ano/mês de Referência',
                            format='%Y-%m',
                            validators=[DataRequired()],
                            )

    planilha = FileField('Planilha',
                            validators=[DataRequired()],
                        )
