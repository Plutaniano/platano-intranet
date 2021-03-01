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

TABELAS_COM_RECEITA = {
    'investimentos': Investimentos,
    'previdencia': Previdencia,
    'cocorretagem': CoCorretagem,
    'banco_xp': BancoXP,
    'cambio': Cambio,
    'incentivo_previdencia': IncentivoPrevidencia
}

DEFAULT_COMISSOES = {
    'RV': 0.25,
    'alocacao': 0.45,
    'previdencia': 0.45,
    'seguros': 0.25,
    'banco_xp': 0.45,
    'cambio': 0.25
}