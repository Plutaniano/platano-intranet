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
  juros_aa = Column('Juros', Integer)
  comissao_escritorio_porcento_aa = Column('Comissão do Escritório', Integer)
  comissao_atualizada_acumulada = Column('Comissão Atualizada Acumulada', Integer)
  deducoes = Column('Deduções', Float)
  total_receita = Column('Receita Total', Integer)

  @classmethod
  def receita_do_escritorio(cls, codigo_a: int, mes_de_entrada: Date) -> int:
    f'''\
      Retorna a receita gerada no seguimento `{cls.__displayname__}` para o escritório pelo `assessor` durante o `mes_de_entrada`.
      Não inclui cálculos de comissão.\
    '''
    query = db.session.query(cls.total_receita).filter_by(codigo_a = codigo_a, mes_de_entrada=mes_de_entrada)
    total = sum(i[0] for i in query)
    return total

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