from openpyxl.worksheet.worksheet import Worksheet
from ..models import db
from ..models.investimentos import Investimentos
from datetime import date, datetime

def parse_investimentos(ws: Worksheet, mes_de_entrada: date) -> None:
    i = 0
    for row in ws.iter_rows():
        print(f"Investimentos: {i}\r", end='')
        if row[0].value not in ['AJUSTES', 'RECEITAS']:
            continue
        
        else:
            entry = Investimentos(mes_de_entrada=mes_de_entrada,
                                  classificacao=row[0].value,
                                  produto=row[1].value,
                                  nivel1=row[2].value,
                                  nivel2=row[3].value,
                                  nivel3=row[4].value,
                                  cliente=int(row[5].value),
                                  master=int(row[6].value[1:]),
                                  data=row[7].value.date(),
                                  receita_bruta=int(100*row[8].value),
                                  receita_liquida=int(100*row[9].value),
                                  comissao_escritorio_porcento=float(0.01*row[10].value),
                                  comissao_escritorio=int(100*row[11].value),
                                  
                                  codigo_a=cell_to_assessor_int(row[13]),
                                  assessor_direto_comissao_porcento=float(0.01*row[14].value),
                                  assessor_direto_comissao=int(100*row[15].value),
                                  
                                  assessor_indireto1_codigo=cell_to_assessor_int(row[17]),
                                  assessor_indireto1_comissao_porcento=float(0.01*row[18].value),
                                  assessor_indireto1_comissao=int(100*row[19].value),
                                  
                                  assessor_indireto2_codigo=cell_to_assessor_int(row[21]),
                                  assessor_indireto2_comissao_porcento=float(0.01*row[22].value),
                                  assessor_indireto2_comissao=int(100*row[23].value),
                                  
                                  assessor_indireto3_codigo=cell_to_assessor_int(row[25]),
                                  assessor_indireto3_comissao_porcento=float(0.01*row[26].value),
                                  assessor_indireto3_comissao=int(100*row[27].value)
                                  )
            db.session.add(entry)
            db.session.commit()
            i += 1
    print('')

def cell_to_assessor_int(cell) -> int:
    if cell.value == '':
        return 0
    
    if cell.value == 'PAN':
        return -1

    else:
        return int(cell.value.replace('A', ''))