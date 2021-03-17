from . import db, Column, func, relationship, ForeignKey
from . import Integer, Float, Date, String

class CoCorretagem(db.Model):
  __tablename__ = 'cocorretagem'
  __displayname__ = 'Co-corretagem'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(20), default='cocorretagem')

  tipo = Column('Tipo', String(30))
  competencia = Column('Competência', Date)
  parceiro = Column('Parceiro', String(60))
  codigo_a = Column('Código A', Integer, ForeignKey('usuarios.Código A'))

  certificado = Column('Certificado', Integer)
  cpf = Column('CPF', String(11))
  codigo_cliente = Column('Código do Cliente', Integer)
  nome_cliente = Column('Nome do Cliente', String(120))

  seguradora = Column('Seguradora', String(30))
  produto = Column('Produto', String(60))
  data_emissao = Column('Data de Emissão', Date)
  reserva = Column('Reserva', Integer)
  tx_adm = Column('Taxa de Administração', Integer)

  taf_base = Column('TAF Base', Integer)
  taf_repasse_porcento = Column(' TAF Repasse', Float)
  taf_receita = Column('TAF Receita', Integer)

  primeira_aplicacao_mensal_base = Column('1a Aplicação Mensal Base', Integer)
  primeira_aplicacao_mensal_repasse = Column('1a Aplicação Mensal Repasse', Float)
  primeira_aplicacao_mensal_receita = Column('1a Aplicação Mensal Receita', Integer)

  aportes_base = Column('Aportes Base', Integer)
  aportes_repasse_porcento = Column('Aportes Repasse', Float)
  aportes_receita = Column('Aportes Receita', Integer)

  portabilidade_base = Column('Portabilidade Base', Integer)
  portabilidade_repasse_porcento = Column('Portabilidade Repasse', Float)
  portabilidade_receita = Column('Portabilidade Receita ', Integer)

  receita_total = Column('Receita Total', Integer)
  obs = Column('Observações', String(100))
  
  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                            cls.produto,
                            func.sum(cls.aportes_base),
                            func.sum(cls.aportes_receita),
                            func.sum(cls.receita_total)
    ).group_by(
                            cls.produto
    ).filter(
                            cls.codigo_a == assessor.codigo_a,
                            cls.mes_de_entrada == mes_de_entrada,
        )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0)]

    return query

