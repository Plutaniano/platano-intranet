from . import db, Column, func, relationship, ForeignKey
from . import Integer, Float, Date, String


class Cambio(db.Model):
  __tablename__ = 'cambio'
  __displayname__ = 'Câmbio'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='cambio')

  codigo_cliente = Column('Código do Cliente', Integer)
  tipo = Column('Tipo', String(20))
  data = Column('Data', Date)
  moeda = Column('Moeda', String(5))
  volume = Column('Volume', Integer)
  receita = Column('Receita', Integer)
  taxa_cliente = Column('Taxa Cliente', Float)
  taxa_base = Column('Taxa Base', Float)
  spread_aplicado = Column('Spread Aplicado', Float)
  codigo_a = Column('Código A', Integer, ForeignKey('usuarios.Código A'))

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.moeda,
                              func.sum(cls.receita)
    ).group_by(
               cls.moeda
    ).filter(
               cls.codigo_a == assessor.codigo_a,
               cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)

    if len(query) == 0:
      return [('-', 0, 0)]

    return query
