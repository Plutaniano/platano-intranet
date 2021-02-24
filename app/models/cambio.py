from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db

class Cambio(db.Model):
  __tablename__ = 'cambio'
  __displayname__ = 'Câmbio'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)

  codigo_cliente = Column('Código do Cliente', Integer)
  tipo = Column('Tipo', String(20))
  data = Column('Data', Date)
  moeda = Column('Moeda', String(5))
  volume = Column('Volume', Integer)
  receita = Column('Receita', Integer)
  taxa_cliente = Column('Taxa Cliente', Float)
  taxa_base = Column('Taxa Base', Float)
  spread_aplicado = Column('Spread Aplicado', Float)
  codigo_a = Column('Código A', Integer)

  @classmethod
  def receita_do_escritorio(cls, codigo_a: int, mes_de_entrada: Date) -> int:
    f'''\
      Retorna a receita gerada no seguimento `{cls.__displayname__}` para o escritório pelo `assessor` durante o `mes_de_entrada`.
      Não inclui cálculos de comissão.\
    '''
    query = db.session.query(cls.receita).filter_by(codigo_a = codigo_a, mes_de_entrada=mes_de_entrada)
    total = sum(i[0] for i in query)
    return total

  showable_columns = [
    (codigo_cliente, lambda x: x, ''),
    (tipo, lambda x: x, ''),
    (data, lambda x: x, ''),
    (moeda, lambda x: x, ''),
    (volume, lambda x: '%.2f' % (0.01 * x), ''),
    (receita, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (taxa_cliente, lambda x: '%.2f' % (0.01 * x), '(%)'),
    (taxa_base, lambda x: '%.2f' % (0.01 * x), '(%)'),
    (spread_aplicado, lambda x: '%.2f' % x, '(%)')
  ]