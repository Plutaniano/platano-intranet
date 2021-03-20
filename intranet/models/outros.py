from . import db


class Outros(db.Model):
  __tablename__ = 'outros'
  __displayname__ = 'Outros'
  
  id = db.Column('ENTRY ID', db.Integer, primary_key=True)
  mes_de_entrada = db.Column('MES DE ENTRADA', db.Date, nullable=False)
  comissionamento = db.Column('COMISSIONAMENTO', db.String(20), default='outros')

  codigo_a = db.Column('Código A', db.Integer, db.ForeignKey('usuarios.Código A'))
  valor = db.Column('Valor', db.Integer)
  descricao = db.Column('Descrição', db.String(120))

  @classmethod
  def consulta(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.descricao,
                              cls.valor
    ).filter(
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    return query

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.descricao,
                              db.literal(0),
                              db.literal(0),
                              db.literal(0),
                              db.literal(1),
                              db.func.sum(cls.valor),
    ).group_by(
               cls.descricao
    ).filter(
               cls.codigo_a == assessor.codigo_a,
               cls.mes_de_entrada == mes_de_entrada,
               cls.valor >= 0
    )

    query = list(query)

    if len(query) == 0:
      return [('-', 0, 0, 0, 1, 0)]

    return query

  @classmethod
  def descontos(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.descricao,
                              db.func.sum(cls.valor)
    ).group_by(
               cls.descricao
    ).filter(
               cls.codigo_a == assessor.codigo_a,
               cls.mes_de_entrada == mes_de_entrada,
               cls.valor < 0
    )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0)]

    return query

  filters = {
    'valor': 'currency'
  }