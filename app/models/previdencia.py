from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db

class Previdencia(db.Model):
  __tablename__ = 'previdencia'
  __displayname__ = 'Previdência'
  # Dados Cliente
  id = Column('ENTRY_ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)

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

  showable_columns = [
    (competencia, lambda x: x.strftime('%Y/%m'), ''),
    (tipo, lambda x: x, ''),
    (certificado, lambda x: x, ''),
    (codigo_cliente, lambda x: x, ''),
    (up, lambda x: x, ''),
    (produto, lambda x: x, ''),
    (receita_bruta_total, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (ir_sobre_receita_bruta, lambda x: '%.2f' % x, '(R$)'),
    (receita_liquida_total, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (obs, lambda x: x, ''),
  ]
