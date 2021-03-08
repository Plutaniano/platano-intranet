import os
from app.models import *

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'my precious'


TABELAS_COM_RECEITA = {
    'investimentos': Investimentos,
    'previdencia': Previdencia,
    'cocorretagem': CoCorretagem,
    'banco_xp': BancoXP,
    'cambio': Cambio
}

DEFAULT_COMISSOES = {
    'rv': 0.25,
    'previdencia': 0.45,
    'seguros': 0.25,
    'banco_xp': 0.45,
    'cambio': 0.25
}

