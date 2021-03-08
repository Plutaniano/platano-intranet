from openpyxl.worksheet.worksheet import Worksheet
from ..models import db
from ..models.previdencia import Previdencia
from datetime import date, datetime

def parse_previdencia(ws: Worksheet, mes_de_entrada: date) -> None:
    i = 0
    for row in ws.iter_rows():
        print(f"Prêvidencia: {i}\r", end='')
        if row[2].value not in ['PLATANO AGENTE AUTONOMO DE INVESTIMENTOS LTDA', 'Platano Investimentos']:
            continue
        
        else:
            if str(row[9].value).startswith('[Devolução '):
                row[28].value = str(row[9].value)
                row[9].value = 'Incentivo Previdência - Adiantamento ROA'
                
            entry = Previdencia(mes_de_entrada=mes_de_entrada,
                                tipo=row[0].value,
                                competencia=row[1].value.date(),
                                parceiro=row[2].value,
                                codigo_a=row[3].value,
                                certificado=row[4].value if isinstance(row[4].value, int) else None,
                                cpf=str(row[5].value),
                                codigo_cliente=row[6].value if isinstance(row[6].value, int) else None,
                                up=str(row[7].value),
                                
                                # Dados do produto
                                seguradora=str(row[8].value),
                                produto=str(row[9].value),
                                data_emissao=row[10].value if isinstance(row[10].value, date) else None,
                                reserva=int(100 * row[11].value if isinstance(row[11].value, float) else 0),
                                tx_adm=float(row[12].value if isinstance(row[12].value, float) else 0),
                                
                                # TAF
                                taf_base=int(100 * row[13].value if isinstance(row[13].value, float) else 0),
                                taf_repasse_porcento=float(row[14].value if isinstance(row[14].value, float) else 0),
                                taf_receita=int(row[15].value if isinstance(row[15].value, int) else 0),
                                
                                # 1a Aplicação Mensal
                                primeira_aplicacao_mensal_base=int(100 * row[16].value if isinstance(row[16].value, float) else 0),
                                primeira_aplicacao_mensal_repasse=float(row[17].value if isinstance(row[17].value, float) else 0),
                                primeira_aplicacao_mensal_receita=int(row[18].value if isinstance(row[18].value, int) else 0),

                                # Aportes/Prêmio
                                aportes_base=int(row[19].value * 100 if isinstance(row[19].value, float) else 0),
                                aportes_repasse_porcento=float(row[20].value if isinstance(row[20].value, float) else 0),
                                aportes_receita=int(100 * row[21].value if isinstance(row[21].value, int) else 0),

                                # Portabilidade
                                portabilidade_base=int(100 * row[22].value if isinstance(row[22].value, float) else 0),
                                portabilidade_repasse_porcento=float(row[23].value if isinstance(row[23].value, float) else 0),
                                portabilidade_receita=int(100 * row[24].value if isinstance(row[24].value, int) else 0),

                                # Receita
                                receita_bruta_total=int(100 * row[25].value),
                                ir_sobre_receita_bruta=int(100 * row[26].value),
                                receita_liquida_total=int(100 * row[27].value),
                                obs=row[28].value or None
                                )
            db.session.add(entry)
            db.session.commit()
            i += 1
    print('')