from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db, Assessor
from typing import Dict

class Previdencia(db.Model):
  __tablename__ = 'previdencia'
  __displayname__ = 'Previdência'

  # Dados Cliente
  id = Column('ENTRY_ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='previdencia')

  tipo = Column('Tipo', String(50))
  competencia = Column('Competencia', Date)
  parceiro = Column('Parceiro', String(60))
  codigo_a = Column('Código A', Integer)
  certificado = Column('Certificado', Integer)
  cpf = Column('CPF', String(11))
  codigo_cliente = Column('Código do Cliente', Integer)
  up = Column('U.P.', String(60))
  
  # Dados do produto
  seguradora = Column('Seguradora', String(30))
  produto = Column('Produto', String(120))
  data_emissao = Column('Data de Contratação/Emissão', Date)
  reserva = Column('Reserva/Capital Segurado', Integer)
  tx_adm = Column('Tx Adm', Float)

  # TAF
  taf_base = Column('TAF Base', Integer)
  taf_repasse_porcento = Column('TAF Repasse', Float)
  taf_receita = Column('TAF Receita (R$)', Integer)
  
  # 1a Aplicacao Mensal
  primeira_aplicacao_mensal_base = Column('1a Aplicação Mensal Base', Integer)
  primeira_aplicacao_mensal_repasse = Column('1a Aplicação Repasse', Float)
  primeira_aplicacao_mensal_receita = Column('1a Aplicação Receita', Integer)

  # Aportes/Premio
  aportes_base = Column('Aportes Base', Integer)
  aportes_repasse_porcento = Column('Aportes Repasse', Float)
  aportes_receita = Column('Aportes Receita', Integer)
  
  # Portabilidade
  portabilidade_base = Column('Portabilidade Base', Integer)
  portabilidade_repasse_porcento = Column('Portabilidade Repasse', Integer)
  portabilidade_receita = Column('Portabilidade Receita', Integer)

  # Receita
  receita_bruta_total = Column('Receita Bruta', Integer)
  ir_sobre_receita_bruta = Column('IR sobre Receita Bruta', Float)
  receita_liquida_total = Column('Receita Líquida Total', Integer)
  obs = Column('Observação', String(120))
  
  @classmethod
  def receita_do_escritorio(cls, codigo_a: int, mes_de_entrada: Date) -> Dict:
    f'''\
      Retorna a receita gerada no seguimento `{cls.__displayname__}` para o escritório pelo `assessor` durante o `mes_de_entrada`.
      Não inclui cálculos de comissão.\
    '''
    receita = {}

    query = db.session.query(cls.aportes_receita, cls.receita_bruta_total, cls.receita_liquida_total).filter_by(codigo_a = codigo_a, mes_de_entrada=mes_de_entrada)
    
    receita['Bruto XP'] = sum(i[0] for i in query)
    receita['Líquido XP'] = sum(i[1] for i in query)
    receita['Escritório'] = sum(i[2] for i in query)

    return receita

  @classmethod
  def descontos(cls, codigo_a: int, mes_de_entrada: Date) -> int:
    query = db.session.query(cls.receita_liquida_total).filter(cls.receita_liquida_total < 0)\
                                                       .filter(cls.mes_de_entrada == mes_de_entrada)\
                                                       .filter(cls.codigo_a == codigo_a)
    return sum(i[0] for i in query)

  showable_columns = [
    (competencia, lambda x: x.strftime('%Y/%m'), ''),
    (tipo, lambda x: x, ''),
    (certificado, lambda x: x, ''),
    (codigo_cliente, lambda x: x, ''),
    (up, lambda x: x, ''),
    (produto, lambda x: x, ''),
    (receita_bruta_total, lambda x: round(0.01 * x, 2), '(R$)'),
    (ir_sobre_receita_bruta, lambda x: round(x, 2), '(R$)'),
    (receita_liquida_total, lambda x: round(0.01 * x, 2), '(R$)'),
    (obs, lambda x: x, ''),
  ]
