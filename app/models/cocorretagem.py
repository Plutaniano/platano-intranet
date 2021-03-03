from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db, Assessor
from typing import Dict


class CoCorretagem(db.Model):
  __tablename__ = 'cocorretagem'
  __displayname__ = 'Co-corretagem'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='cocorretagem')

  tipo = Column('Tipo', String(30))
  competencia = Column('Competência', Date)
  parceiro = Column('Parceiro', String(60))
  codigo_a = Column('Código A', Integer)

  certificado = Column('Certificado', Integer)
  cpf = Column('CPF', String(11))
  codigo_cliente = Column('Código do Cliente', Integer)
  nome_cliente = Column('Nome do Cliente', String(120))

  seguradora = Column('Seguradora', String(30))
  produto = Column('Produto', String(60))
  data_emissao = Column('Data de Emissão', Date)
  reserva = Column('Reserva', Integer)
  tx_adm = Column('Taxa de Administração', Integer)

  taf_base = Column('TAF Base', Integer)
  taf_repasse_porcento = Column(' TAF Repasse', Float)
  taf_receita = Column('TAF Receita', Integer)

  primeira_aplicacao_mensal_base = Column('1a Aplicação Mensal Base', Integer)
  primeira_aplicacao_mensal_repasse = Column('1a Aplicação Mensal Repasse', Float)
  primeira_aplicacao_mensal_receita = Column('1a Aplicação Mensal Receita', Integer)

  aportes_base = Column('Aportes Base', Integer)
  aportes_repasse_porcento = Column('Aportes Repasse', Float)
  aportes_receita = Column('Aportes Receita', Integer)

  portabilidade_base = Column('Portabilidade Base', Integer)
  portabilidade_repasse_porcento = Column('Portabilidade Repasse', Float)
  portabilidade_receita = Column('Portabilidade Receita ', Integer)

  receita_total = Column('Receita Total', Integer)
  obs = Column('Observações', String(100))
  
  @classmethod
  def receita_do_escritorio(cls, codigo_a: int, mes_de_entrada: Date) -> Dict:
    f'''\
      Retorna a receita gerada no seguimento `{cls.__displayname__}` para o escritório pelo `assessor` durante o `mes_de_entrada`.
      Não inclui cálculos de comissão.\
    '''
    receita = {}

    query = db.session.query(cls.aportes_base, cls.aportes_receita, cls.receita_total).filter_by(codigo_a = codigo_a, mes_de_entrada=mes_de_entrada)
    
    receita['Bruto XP'] = sum(i[0] for i in query)
    receita['Líquido XP'] = sum(i[1] for i in query)
    receita['Escritório'] = sum(i[2] for i in query)

    return receita

  showable_columns = [
    (tipo, lambda x: x, ''),
    (certificado, lambda x: x, ''),
    (codigo_cliente, lambda x: x, ''),
    (produto, lambda x: x, ''),
    (data_emissao, lambda x: x.strftime('%Y/%m'), ''),
    (aportes_base, lambda x: '%.2f' % x, '(R$)'),
    (aportes_repasse_porcento, lambda x: '%.0f' % x, '(%)'),
    (aportes_receita, lambda x: '%.2f' % x, '(R$)'),
    (receita_total, lambda x: '%.2f' % (0.01 * x), '(R$)')
  ]
