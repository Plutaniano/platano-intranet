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

  showable_columns = [
    (codigo_cliente, lambda x: x, ''),
    (tipo, lambda x: x, ''),
    (data, lambda x: x, ''),
    (moeda, lambda x: x, ''),
    (volume, lambda x: round(0.01 * x, 2), ''),
    (receita, lambda x: round(0.01 * x, 2), '(R$)'),
    (taxa_cliente, lambda x: round(0.01 * x, 2), '(%)'),
    (taxa_base, lambda x: round(0.01 * x, 2), '(%)'),
    (spread_aplicado, lambda x: round(x, 2), '(%)')
  ]