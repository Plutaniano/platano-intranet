from . import db

class BancoXP(db.Model):
  __tablename__ = 'banco_xp'
  __displayname__ = 'Banco XP'
  id= db.Column('ENTRY ID', db.Integer, primary_key=True)
  mes_de_entrada= db.Column('MES DE ENTRADA', db.Date)
  comissionamento= db.Column('COMISSIONAMENTO', db.String(20), default='banco_xp')

  competencia= db.Column('Competência', db.Date)
  codigo_escritorio= db.Column('Código do Escritório', db.Integer)
  parceiro= db.Column('Parceiro', db.String(60))
  codigo_a= db.Column('Código A', db.Integer, db.ForeignKey('usuarios.Código A'))
  operacao= db.Column('Operação', db.Integer)
  codigo_cliente= db.Column('Código do Cliente', db.Integer)
  produto= db.Column('Produto', db.String(60))
  data_contratacao= db.Column('Data de Contratação', db.Date)
  data_vencimento= db.Column('Data de Vencimento', db.Date)
  valor_contratado= db.Column('Valor da Contratação', db.Integer)
  juros_aa= db.Column('Juros', db.Integer)
  comissao_escritorio_porcento_aa= db.Column('Comissão do Escritório', db.Integer)
  comissao_atualizada_acumulada= db.Column('Comissão Atualizada Acumulada', db.Integer)
  deducoes= db.Column('Deduções', db.Float)
  total_receita= db.Column('Receita Total', db.Integer)

  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                            cls.produto,
                            db.literal(0),
                            db.func.sum(cls.comissao_atualizada_acumulada),
                            db.func.sum(cls.total_receita),
                            db.literal(assessor.comissao_bancoxp),
                            db.func.sum(cls.total_receita) * db.literal(assessor.comissao_bancoxp),
    ).group_by(
                            cls.produto
    ).filter(
                            cls.codigo_a == assessor.codigo_a,
                            cls.mes_de_entrada == mes_de_entrada,
        )

    query = list(query)

    if len(query) == 0:
      return [('-', 0, 0, 0, assessor.comissao_bancoxp, 0)]

    return query


  @classmethod
  def consulta(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.id,
                              cls.codigo_cliente,
                              cls.produto,
                              cls.data_contratacao,
                              cls.data_vencimento,
                              cls.valor_contratado,
                              cls.juros_aa,
                              cls.comissao_escritorio_porcento_aa,
                              cls.comissao_atualizada_acumulada,
                              cls.deducoes,
                              cls.total_receita
    ).filter(
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    return query

  filters = {
    'data_contratacao': 'date',
    'data_vencimento': 'date',
    'valor_contratado': 'currency',
    'juros_aa': 'percent',
    'comissao_escritorio_porcento_aa': 'percent',
    'comissao_atualizada_acumulada': 'currency',
    'deducoes': 'percent',
    'total_receita': 'currency'
  }
