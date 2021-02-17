from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db


class BancoXP(db.Model):
  __tablename__ = 'banco_xp'
  __displayname__ = 'Banco XP'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)

  competencia = Column('Competência', Date)
  codigo_escritorio = Column('Código do Escritório', Integer)
  parceiro = Column('Parceiro', String(60))
  codigo_a = Column('Código A', Integer)
  operacao = Column('Operação', Integer)
  codigo_cliente = Column('Código do Cliente', Integer)
  produto = Column('Produto', String(60))
  data_contratacao = Column('Data de Contratação', Date)
  data_vencimento = Column('Data de Vencimento', Date)
  valor_contratado = Column('Valor da Contratação', Integer)
  juros_aa = Column('Juros a.a.', Integer)
  comissao_escritorio_porcento_aa = Column('Comissão do Escritório a.a.', Integer)
  comissao_atualizada_acumulada = Column('Comissão Atualizada Acumulada', Integer)
  deducoes = Column('Deduções', Float)
  total_receita = Column('Receita Total', Integer)

  showable_columns = [
    (codigo_cliente, lambda x: x, ''),
    (produto, lambda x: x, ''),
    (data_contratacao, lambda x: x.strftime('%Y/%m/%d'), ''),
    (data_vencimento, lambda x: x.strftime('%Y/%m/%d'), ''),
    (valor_contratado, lambda x: round(0.01 * x, 2), '(R$)'),
    (juros_aa, lambda x: round(100 * x, 2), '(%)'),
    (comissao_escritorio_porcento_aa, lambda x: round(100 * x, 2), '(%aa)'),
    (comissao_atualizada_acumulada, lambda x: round(0.01 * x, 2), '(R$)'),
    (deducoes, lambda x: 100 * x, '(R$)'),
    (total_receita, lambda x: round(0.01 * x, 2), '(R$)')
  ]