import datetime

from openpyxl.worksheet.worksheet import Worksheet

from ..models import db
from ..models.bancoxp import BancoXP

def parse_banco_xp(ws: Worksheet, mes_de_entrada: datetime.date) -> None:
    i = 0
    for row in ws.iter_rows():
        print(f"Banco XP: {i}\r", end='')
        if not isinstance(row[0].value, datetime.date):
            continue
        
        else:
            entry = BancoXP(mes_de_entrada=mes_de_entrada,
                            competencia=row[0].value.date(),
                            codigo_escritorio=row[1].value,
                            parceiro=row[2].value,
                            codigo_a=row[3].value if isinstance(row[3].value, int) else str(row[3].value)[1:],
                            operacao=row[4].value,
                            codigo_cliente=row[5].value,
                            produto=row[6].value,
                            data_contratacao=row[7].value,
                            data_vencimento=row[8].value,
                            valor_contratado=int(100 * row[9].value),
                            juros_aa=float(row[10].value),
                            comissao_escritorio_porcento_aa=float(row[11].value),
                            comissao_atualizada_acumulada=int(100 * row[12].value),
                            deducoes=float(row[13].value),
                            total_receita=int(100 * row[14].value)
                            )
            db.session.add(entry)
            db.session.commit()
            i += 1
    print('')