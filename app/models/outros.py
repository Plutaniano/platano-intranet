from . import db, Column, func, relationship, ForeignKey
from . import Integer, Float, Date, String

class Outros(db.Model):
  __tablename__ = 'outros'
  __displayname__ = 'Outros'
  
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date, nullable=False)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='outros')

  codigo_a = Column('Código A', Integer, ForeignKey('usuarios.Código A'))
  valor = Column('Valor', Integer)
  descricao = Column('Descrição', String(120))

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.descricao,
                              func.sum(cls.valor),
    ).group_by(
               cls.descricao
    ).filter(
               cls.codigo_a == assessor.codigo_a,
               cls.mes_de_entrada == mes_de_entrada,
               cls.valor >= 0
    )

    query = list(query)

    if len(query) == 0:
      return [('-', 0, 0)]

    return query

  @classmethod
  def descontos(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.descricao,
                              func.sum(cls.valor)
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

  showable_columns = [
    (codigo_a, lambda x: x, ''),
    (valor, lambda x: x, ''),
    (descricao, lambda x: x, '')
  ]