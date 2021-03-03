from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db, Assessor
from flask import current_app
from typing import Dict



class Investimentos(db.Model):
  __tablename__ = 'investimentos'
  __displayname__ = 'Investimentos'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='RV')
  
  classificacao = Column('Classificação', String(20))
  produto = Column('Produto', String(50))
  nivel1 = Column('Nível 1', String(200))
  nivel2 = Column('Nível 2', String(50))
  nivel3 = Column('Nível 3', String(50))
  cliente = Column('Código do Cliente', Integer)
  master = Column('Código Master', Integer)
  data = Column('Data', Date)
  receita_bruta = Column('Receita Bruta', Integer)
  receita_liquida = Column('Receita Líquida', Integer)
  comissao_escritorio = Column('Comissão do Escritório', Integer)
  comissao_escritorio_porcento = Column('Comissão Relativa do Escritório', Float) 
  
  codigo_a = Column('Código A', Integer)
  assessor_direto_comissao_porcento = Column('Assessor Direto', Integer)
  assessor_direto_comissao = Column('Assessor Direto Comissão', Integer)

  assessor_indireto1_codigo = Column('Assessor Indireto 1 Código', Integer)
  assessor_indireto1_comissao_porcento = Column('Assessor Indireto 1', Integer)
  assessor_indireto1_comissao = Column('Assessor Indireto 1 Comissão', Integer)

  assessor_indireto2_codigo = Column('Assessor Indireto 2 Código', Integer)
  assessor_indireto2_comissao_porcento = Column('Assessor Indireto 2', Integer)
  assessor_indireto2_comissao = Column('Assessor Indireto 2 Comissão', Integer)

  assessor_indireto3_codigo = Column('Assessor Indireto 3 Código', Integer)
  assessor_indireto3_comissao_porcento = Column('Assessor Indireto 3', Integer)
  assessor_indireto3_comissao = Column('Assessor Indireto 3 Comissão', Integer)

  @classmethod
  def receita_do_escritorio(cls, codigo_a: int, mes_de_entrada: Date) -> Dict:
    f'''\
      Retorna a receita gerada no seguimento `{cls.__displayname__}` para o escritório pelo `assessor` durante o `mes_de_entrada`.
      Não inclui cálculos de comissão.\
    '''
    receita = {}

    query = db.session.query(cls.receita_bruta, cls.receita_liquida, cls.comissao_escritorio)\
                      .filter_by(codigo_a = codigo_a, mes_de_entrada=mes_de_entrada)\
                      .filter(cls.comissao_escritorio >= 0)

    receita['Bruto XP'] = sum(i[0] for i in query)
    receita['Líquido XP'] = sum(i[1] for i in query)
    receita['Escritório'] = sum(i[2] for i in query)

    return receita
  
  @classmethod
  def descontos(cls, codigo_a: int, mes_de_entrada: Date) -> int:
    query = db.session.query(cls.comissao_escritorio)\
                        .filter(cls.codigo_a == codigo_a)\
                        .filter(cls.comissao_escritorio < 0)\
                        .filter(cls.mes_de_entrada == mes_de_entrada)
    return sum(i[0] for i in query)

  showable_columns = [
    # (coluna, função para display, unidade)
    (classificacao,               lambda x: x, ''),
    (produto,                     lambda x: x, ''),
    (nivel1,                      lambda x: x, ''),
    (nivel2,                      lambda x: x, ''),
    (cliente,                     lambda x: x, ''),
    (data,                        lambda x: x.strftime('%Y/%m/%d'), ''),
    (receita_bruta,               lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (receita_liquida,             lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (comissao_escritorio_porcento,lambda x: '%.2f' % (100 * x), '(%)'),
    (comissao_escritorio,         lambda x: '%.2f' % (0.01 * x), '(R$)')
  ]