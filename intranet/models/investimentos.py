from . import db

class Investimentos(db.Model):
  __tablename__ = 'investimentos'
  __displayname__ = 'Investimentos'
  id = db.Column('ENTRY ID', db.Integer, primary_key=True)
  mes_de_entrada= db.Column('MES DE ENTRADA', db.Date)
  comissionamento= db.Column('COMISSIONAMENTO', db.String(20), default='RV')
  
  classificacao= db.Column('Classificação', db.String(20))
  produto= db.Column('Produto', db.String(50))
  nivel1= db.Column('Nível 1', db.String(200))
  nivel2= db.Column('Nível 2', db.String(50))
  nivel3= db.Column('Nível 3', db.String(50))
  cliente= db.Column('Código do Cliente', db.Integer)
  master= db.Column('Código Master', db.Integer)
  data= db.Column('Data', db.Date)
  receita_bruta= db.Column('Receita Bruta', db.Integer)
  receita_liquida= db.Column('Receita Líquida', db.Integer)
  comissao_escritorio= db.Column('Comissão do Escritório', db.Integer)
  comissao_escritorio_porcento= db.Column('Comissão Relativa do Escritório', db.Float) 
  
  codigo_a= db.Column('Código A', db.Integer, db.ForeignKey('usuarios.Código A'))
  assessor_direto_comissao_porcento= db.Column('Assessor Direto', db.Integer)
  assessor_direto_comissao= db.Column('Assessor Direto Comissão', db.Integer)

  assessor_indireto1_codigo= db.Column('Assessor Indireto 1 Código', db.Integer)
  assessor_indireto1_comissao_porcento= db.Column('Assessor Indireto 1', db.Integer)
  assessor_indireto1_comissao= db.Column('Assessor Indireto 1 Comissão', db.Integer)

  assessor_indireto2_codigo= db.Column('Assessor Indireto 2 Código', db.Integer)
  assessor_indireto2_comissao_porcento= db.Column('Assessor Indireto 2', db.Integer)
  assessor_indireto2_comissao= db.Column('Assessor Indireto 2 Comissão', db.Integer)

  assessor_indireto3_codigo= db.Column('Assessor Indireto 3 Código', db.Integer)
  assessor_indireto3_comissao_porcento= db.Column('Assessor Indireto 3', db.Integer)
  assessor_indireto3_comissao= db.Column('Assessor Indireto 3 Comissão', db.Integer)

  @classmethod
  def receitas_rv(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.produto,
                              db.func.sum(cls.receita_bruta),
                              db.func.sum(cls.receita_liquida),
                              db.func.sum(cls.comissao_escritorio),
                              db.literal(assessor.comissao_rv),
                              db.func.sum(cls.comissao_escritorio) * db.literal(assessor.comissao_rv)
    ).group_by(
                              cls.produto
    ).filter(
                              cls.produto.notin_(cls.ALOCACAO),
                              cls.produto.notin_(cls.DESCONTOS),
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0, 0, 0)]

    return query

  @classmethod
  def receitas_alocacao(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.produto,
                              db.func.sum(cls.receita_bruta),
                              db.func.sum(cls.receita_liquida),
                              db.func.sum(cls.comissao_escritorio),
                              db.literal(assessor.comissao_alocacao),
                              db.func.sum(cls.comissao_escritorio) * db.literal(assessor.comissao_alocacao)
    ).group_by(
                              cls.produto
    ).filter(
                              cls.produto.in_(cls.ALOCACAO),
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0, 0, 0)]

    return query

  
  @classmethod
  def descontos(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.produto,
                              db.func.sum(cls.comissao_escritorio)
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
    'Erro Operacional'
  ]