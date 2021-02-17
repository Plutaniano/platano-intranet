from openpyxl.worksheet.worksheet import Worksheet
from ..models import db
from ..models.cambio import Cambio
from datetime import date, datetime

def parse_cambio(ws: Worksheet, mes_de_entrada: date) -> None:
    i = 0
    for row in ws.iter_rows():
        print(f"Câmbio: {i}\r", end='')
        if row[1].value not in ['Compra', 'Venda']:
            continue
        
        else:
            entry = Cambio(     mes_de_entrada=mes_de_entrada,
                                codigo_cliente=row[0].value,
                                tipo=row[1].value,
                                data=row[2].value.date() if isinstance(row[2].value, datetime) else date(int(row[2].value.split('/')[2]), int(row[2].value.split('/')[1]), 1),
                                moeda=str(row[3].value),
                                volume=int(100 * row[4].value),
                                receita=int(100 * row[5].value),
                                taxa_cliente=int(100 * row[6].value),
                                taxa_base=int(100 * row[7].value),
                                spread_aplicado=float(row[8].value),
                                codigo_a=int(row[10].value[1:])
                                )
            db.session.add(entry)
            db.session.commit()
            i += 1
    print('')