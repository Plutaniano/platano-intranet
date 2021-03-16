from sqlalchemy import Integer, String, Float, Date, Column, func

from . import db


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
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.produto,
                              func.sum(cls.receita_bruta),
                              func.sum(cls.receita_liquida),
                              func.sum(cls.comissao_escritorio)
    ).group_by(
                              cls.produto
    ).filter(
                              cls.produto.in_(cls.RV),
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0)]

    return query

  @classmethod
  def receitas_alocacao(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.produto,
                              func.sum(cls.receita_bruta),
                              func.sum(cls.receita_liquida),
                              func.sum(cls.comissao_escritorio)
    ).group_by(
                              cls.produto
    ).filter(
                              cls.produto.in_(cls.ALOCACAO),
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0)]

    return query

  
  @classmethod
  def descontos(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.produto,
                              func.sum(cls.comissao_escritorio)
    ).group_by(
                              cls.produto
    ).filter(
                              cls.produto.in_(cls.DESCONTOS),
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)
    if len(query) == 0:
      return [('-', 0)]

    return query

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

  RV = [
    'BMF MINI',
    'BM&F',
    'BMF SELF SERVICE',
    'BOVESPA SELF SERVICE',
    'BOVESPA',
    'CLUBES',
    'BTC',
    'IPO',
    'OFERTA RV',
    'OFERTA FII',
    'COMPLEMENTO DE CORRETAGEM',
    'INDICAÇÃO DE CLIENTES',
    'Transferencia de Clientes',
    'Campanha Fundos Imobiliários'
  ]

  ALOCACAO = [
    'COE',
    'FUNDOS - TX ADM',
    'IPO FEE RENDA FIXA',
    'RENDA FIXA',
    'FUNDOS - TX PERF',
    'Campanha Fundos',
    'Campanha Renda Fixa',
  ]

  DESCONTOS = [
    'Enquadramento RLP',  
    'Clubes (debito)',
    'Erro Operacional'
  ]