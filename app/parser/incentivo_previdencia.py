from openpyxl.worksheet.worksheet import Worksheet
from ..models import db
from ..models.incentivo_previdencia import IncentivoPrevidencia
from datetime import date, datetime

def parse_incentivo_previdencia(ws: Worksheet, mes_de_entrada: date) -> None:
    i = 0
    for row in ws.iter_rows():
        print(f"Incentivo Previdência: {i}\r", end='')
        if not isinstance(row[0].value, date):
            continue
        
        else:
            entry = IncentivoPrevidencia(mes_de_entrada=mes_de_entrada,
                                mes_referencia=row[0].value,
                                status_docusign=row[1] == 'Assinado',
                                codigo_escritorio=row[2].value,
                                escritorio=row[3].value,
                                codigo_a=row[4].value,
                                codigo_cliente=row[5].value,
                                certificado=row[6].value,
                                movimentacao_cliente=int(100 * row[7].value),
                                adiantamento_previdencia=int(100 * row[8].value)
                                )
            db.session.add(entry)
            db.session.commit()
            i += 1
    print('')