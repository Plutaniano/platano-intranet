from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Integer = db.Integer
Float = db.Float
String = db.String
Column = db.Column
Date = db.Date
Boolean = db.Boolean
relationship = db.relationship
ForeignKey = db.ForeignKey
func = db.func
literal = db.literal
case = db.case

from .usuario import Usuario
from .clientes import Cliente
from .investimentos import Investimentos
from .previdencia import Previdencia
from .cambio import Cambio
from .cocorretagem import CoCorretagem
from .bancoxp import BancoXP
from .outros import Outros

SEGMENTOS = [
    Investimentos,
    Previdencia,
    Cambio,
    CoCorretagem,
    BancoXP
]