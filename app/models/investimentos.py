from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db



class Investimentos(db.Model):
  __tablename__ = 'investimentos'
  __displayname__ = 'Investimentos'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  
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

  showable_columns = [
    # (coluna, função para display)
    (classificacao, lambda x: x, ''),
    (produto, lambda x: x, ''),
    (nivel1, lambda x: x, ''),
    (nivel2, lambda x: x, ''),
    (cliente, lambda x: x, ''),
    (data, lambda x: x.strftime('%Y/%m/%d'), ''),
    (receita_bruta, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (receita_liquida, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (comissao_escritorio_porcento, lambda x: '%.0f' % (100 * x), '(%)'),
    (comissao_escritorio, lambda x: '%.2f' % (0.01 * x), '(R$)'),
  ]