from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .assessor import Assessor
from .investimentos import Investimentos
from .previdencia import Previdencia
from .cambio import Cambio
from .incentivo_previdencia import IncentivoPrevidencia
from .cocorretagem import CoCorretagem
from .bancoxp import BancoXP

