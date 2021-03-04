from sqlalchemy import Integer, String, Float, Boolean, Date, Column, func, ForeignKey
from . import db
from typing import Dict


class BancoXP(db.Model):
  __tablename__ = 'banco_xp'
  __displayname__ = 'Banco XP'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='banco_xp')

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
  juros_aa = Column('Juros', Integer)
  comissao_escritorio_porcento_aa = Column('Comissão do Escritório', Integer)
  comissao_atualizada_acumulada = Column('Comissão Atualizada Acumulada', Integer)
  deducoes = Column('Deduções', Float)
  total_receita = Column('Receita Total', Integer)

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                            cls.produto,
                            func.sum(cls.comissao_atualizada_acumulada),
                            func.sum(cls.total_receita)
    ).group_by(
                            cls.produto
    ).filter(
                            cls.codigo_a == assessor.codigo_a,
                            cls.mes_de_entrada == mes_de_entrada,
        )

    query = list(query)

    if len(query) == 0:
      return [('-', 0, 0)]

    return query

  showable_columns = [
    (codigo_cliente, lambda x: x, ''),
    (produto, lambda x: x, ''),
    (data_contratacao, lambda x: x.strftime('%Y/%m/%d'), ''),
    (data_vencimento, lambda x: x.strftime('%Y/%m/%d'), ''),
    (valor_contratado, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (juros_aa, lambda x: '%.2f' % (100 * x), '(%)'),
    (comissao_escritorio_porcento_aa, lambda x: '%.2f' % (100 * x), '(%aa)'),
    (comissao_atualizada_acumulada, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (deducoes, lambda x: '%.2f' % (100 * x), '(R$)'),
    (total_receita, lambda x: '%.2f' % (0.01 * x), '(R$)')
  ]