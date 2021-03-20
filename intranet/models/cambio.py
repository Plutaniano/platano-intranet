from . import db

class Cambio(db.Model):
  __tablename__ = 'cambio'
  __displayname__ = 'Câmbio'
  id= db.Column('ENTRY ID', db.Integer, primary_key=True)
  mes_de_entrada= db.Column('MES DE ENTRADA', db.Date)
  comissionamento= db.Column('COMISSIONAMENTO', db.String(20), default='cambio')

  codigo_cliente= db.Column('Código do Cliente', db.Integer)
  tipo= db.Column('Tipo', db.String(20))
  data= db.Column('Data', db.Date)
  moeda= db.Column('Moeda', db.String(5))
  volume= db.Column('Volume', db.Integer)
  receita= db.Column('Receita', db.Integer)
  taxa_cliente= db.Column('Taxa Cliente', db.Float)
  taxa_base= db.Column('Taxa Base', db.Float)
  spread_aplicado= db.Column('Spread Aplicado', db.Float)
  codigo_a= db.Column('Código A', db.Integer, db.ForeignKey('usuarios.Código A'))

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.moeda,
                              db.literal(0),
                              db.literal(0),
                              db.func.sum(cls.receita),
                              db.literal(assessor.comissao_cambio),
                              db.func.sum(cls.receita) * db.literal(assessor.comissao_cambio),
    ).group_by(
               cls.moeda
    ).filter(
               cls.codigo_a == assessor.codigo_a,
               cls.mes_de_entrada == mes_de_entrada
    )

    query = list(query)

    if len(query) == 0:
      return [('-', 0, 0, 0, assessor.comissao_cambio, 0)]

    return query
  
  @classmethod
  def consulta(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.id,
                              cls.codigo_cliente,
                              cls.tipo,
                              cls.data,
                              cls.moeda,
                              cls.volume,
                              cls.receita,
                              cls.taxa_cliente,
                              cls.taxa_base,
                              cls.spread_aplicado,
    ).filter(
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    return query

  filters = {
    'data': 'date',
    'volume': 'currency',
    'receita': 'currency',
    'taxa_cliente': 'percent',
    'taxa_base': 'percent',
    'spread_aplicado': 'percent'
  }