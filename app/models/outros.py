from sqlalchemy import Integer, String, Date, Column, func

from . import db

class Outros(db.Model):
  __tablename__ = 'outros'
  __displayname__ = 'Outros'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='outros')

  codigo_a = Column('Código A', Integer)
  valor = Column('Valor', Integer)
  descricao = Column('Descrição', String(120))

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.descricao.label('Descrição'),\
                              func.sum(cls.valor.label('Valor'))\
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
                              cls.descricao.label('Descrição'),\
                              func.sum(cls.valor.label('Valor'))\
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