import os
from app.models import *

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'my precious'


IMPOSTOS = {
    'ISS': 0.05,
    'PIS': 0.0065,
    'COFINS': 0.03,
    'IRPJ': 0.0736,
    'CSLL': 0.0288
}

TABELAS_COM_RECEITA = [
    Investimentos,
    Previdencia,
    CoCorretagem,
    BancoXP,
    Cambio,
    IncentivoPrevidencia
]