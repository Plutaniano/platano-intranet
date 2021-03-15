from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .investimentos import Investimentos
from .previdencia import Previdencia
from .cambio import Cambio
from .cocorretagem import CoCorretagem
from .bancoxp import BancoXP
from .outros import Outros
from .assessor import Assessor


SEGMENTOS = [
    Investimentos,
    Previdencia,
    Cambio,
    CoCorretagem,
    BancoXP
]