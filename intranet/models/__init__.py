from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .usuario import Usuario
from .clientes import Cliente
from .investimentos import Investimentos
from .previdencia import Previdencia
from .cambio import Cambio
from .cocorretagem import CoCorretagem
from .bancoxp import BancoXP
from .outros import Outros

TABELAS_COM_RECEITA = {
    'investimentos': Investimentos,
    'previdencia': Previdencia,
    'cocorretagem': CoCorretagem,
    'banco_xp': BancoXP,
    'cambio': Cambio,
    'outros': Outros
}