from . import db

class CoCorretagem(db.Model):
  __tablename__ = 'cocorretagem'
  __displayname__ = 'Co-corretagem'
  id = db.Column('ENTRY ID', db.Integer, primary_key=True)
  mes_de_entrada = db.Column('MES DE ENTRADA', db.Date)
  comissionamento = db.Column('COMISSIONAMENTO', db.String(20), default='cocorretagem')

  tipo = db.Column('Tipo', db.String(30))
  competencia = db.Column('Competência', db.Date)
  parceiro = db.Column('Parceiro', db.String(60))
  codigo_a = db.Column('Código A', db.Integer, db.ForeignKey('usuarios.Código A'))

  certificado = db.Column('Certificado', db.Integer)
  cpf = db.Column('CPF', db.String(11))
  codigo_cliente = db.Column('Código do Cliente', db.Integer)
  nome_cliente = db.Column('Nome do Cliente', db.String(120))

  seguradora = db.Column('Seguradora', db.String(30))
  produto = db.Column('Produto', db.String(60))
  data_emissao = db.Column('Data de Emissão', db.Date)
  reserva = db.Column('Reserva', db.Integer)
  tx_adm = db.Column('Taxa de Administração', db.Integer)

  taf_base = db.Column('TAF Base', db.Integer)
  taf_repasse_porcento = db.Column(' TAF Repasse', db.Float)
  taf_receita = db.Column('TAF Receita', db.Integer)

  primeira_aplicacao_mensal_base = db.Column('1a Aplicação Mensal Base', db.Integer)
  primeira_aplicacao_mensal_repasse = db.Column('1a Aplicação Mensal Repasse', db.Float)
  primeira_aplicacao_mensal_receita = db.Column('1a Aplicação Mensal Receita', db.Integer)

  aportes_base = db.Column('Aportes Base', db.Integer)
  aportes_repasse_porcento = db.Column('Aportes Repasse', db.Float)
  aportes_receita = db.Column('Aportes Receita', db.Integer)

  portabilidade_base = db.Column('Portabilidade Base', db.Integer)
  portabilidade_repasse_porcento = db.Column('Portabilidade Repasse', db.Float)
  portabilidade_receita = db.Column('Portabilidade Receita ', db.Integer)

  receita_total = db.Column('Receita Total', db.Integer)
  obs = db.Column('Observações', db.String(100))
  
  
  @classmethod
  def consulta(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.id,
                              cls.tipo,
                              cls.certificado,
                              cls.codigo_cliente,
                              cls.produto,
                              cls.data_emissao,
                              cls.aportes_base,
                              cls.aportes_repasse_porcento,
                              cls.aportes_receita,
                              cls.receita_total,
                              cls.obs
    ).filter(
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    return query
  
  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    query = db.session.query(
                            cls.produto,
                            db.func.sum(cls.aportes_base),
                            db.func.sum(cls.aportes_receita),
                            db.func.sum(cls.receita_total),
                            db.literal(1), # comissão cocorretagem??
                            db.func.sum(cls.receita_total) * db.literal(1)
    ).group_by(
                            cls.produto
    ).filter(
                            cls.codigo_a == assessor.codigo_a,
                            cls.mes_de_entrada == mes_de_entrada,
        )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0, 1, 0)]

    return query

  filters = {
    'data_emissao': 'date',
    'aportes_base': 'currency',
    'aportes_repasse_porcent': 'percent',
    'aportes_receita': 'currency',
    'receita_total': 'currency',
  }
