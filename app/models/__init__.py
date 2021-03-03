from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .assessor import Assessor
from .investimentos import Investimentos
from .previdencia import Previdencia
from .cambio import Cambio
from .cocorretagem import CoCorretagem
from .bancoxp import BancoXP

SEGMENTOS = [
    Investimentos,
    Previdencia,
    Cambio,
    CoCorretagem,
    BancoXP
]