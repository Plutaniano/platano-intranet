from ..models import *
from typing import List, Tuple

queries = [
            Investimentos.data,
            Previdencia.competencia,
            CoCorretagem.competencia,
            IncentivoPrevidencia.mes_referencia,
            Cambio.data,
            BancoXP.competencia
        ]

def get_date_choices() -> List[Tuple[str, str]]:
    choices = set()

    for q in queries:
        q = db.session.query(q)
        for data in q:
            try:
                choices.add(data.replace(day=1))
            except: 
                print('ERRO: ' + data)