import os
from intranet.models import *

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
    'cambio': Cambio,
    'outros': Outros
}