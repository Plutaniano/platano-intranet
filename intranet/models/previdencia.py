from . import db

class Previdencia(db.Model):
  __tablename__ = 'previdencia'
  __displayname__ = 'Previdência'

  # Dados Cliente
  id = db.Column('ENTRY_ID', db.Integer, primary_key=True)
  mes_de_entrada = db.Column('MES DE ENTRADA', db.Date)
  comissionamento = db.Column('COMISSIONAMENTO', db.String(20), default='previdencia')

  tipo = db.Column('Tipo', db.String(50))
  competencia = db.Column('Competencia', db.Date)
  parceiro = db.Column('Parceiro', db.String(60))
  codigo_a = db.Column('Código A', db.Integer, db.ForeignKey('usuarios.Código A'))
  certificado = db.Column('Certificado', db.Integer)
  cpf = db.Column('CPF', db.String(11))
  codigo_cliente = db.Column('Código do Cliente', db.Integer)
  up = db.Column('U.P.', db.String(60))
  
  # Dados do produto
  seguradora = db.Column('Seguradora', db.String(30))
  produto = db.Column('Produto', db.String(120))
  data_emissao = db.Column('Data de Contratação/Emissão', db.Date)
  reserva = db.Column('Reserva/Capital Segurado', db.Integer)
  tx_adm = db.Column('Tx Adm', db.Float)

  # TAF
  taf_base = db.Column('TAF Base', db.Integer)
  taf_repasse_porcento = db.Column('TAF Repasse', db.Float)
  taf_receita = db.Column('TAF Receita (R$)', db.Integer)
  
  # 1a Aplicacao Mensal
  primeira_aplicacao_mensal_base = db.Column('1a Aplicação Mensal Base', db.Integer)
  primeira_aplicacao_mensal_repasse = db.Column('1a Aplicação Repasse', db.Float)
  primeira_aplicacao_mensal_receita = db.Column('1a Aplicação Receita', db.Integer)

  # Aportes/Premio
  aportes_base = db.Column('Aportes Base', db.Integer)
  aportes_repasse_porcento = db.Column('Aportes Repasse', db.Float)
  aportes_receita = db.Column('Aportes Receita', db.Integer)
  
  # Portabilidade
  portabilidade_base = db.Column('Portabilidade Base', db.Integer)
  portabilidade_repasse_porcento = db.Column('Portabilidade Repasse', db.Integer)
  portabilidade_receita = db.Column('Portabilidade Receita', db.Integer)

  # Receita
  receita_bruta_total = db.Column('Receita Bruta', db.Integer)
  ir_sobre_receita_bruta = db.Column('IR sobre Receita Bruta', db.Integer)
  receita_liquida_total = db.Column('Receita Líquida Total', db.Integer)
  obs = db.Column('Observação', db.String(120))
  

  @classmethod
  def consulta(cls, assessor, mes_de_entrada):
    query = db.session.query(
                              cls.tipo,
                              cls.certificado,
                              cls.up,
                              cls.produto,
                              cls.receita_bruta_total,
                              cls.ir_sobre_receita_bruta,
                              cls.receita_liquida_total,
                              cls.obs
    ).filter(
                              cls.codigo_a == assessor.codigo_a,
                              cls.mes_de_entrada == mes_de_entrada
    )

    return query


  @classmethod
  def receitas(cls, assessor, mes_de_entrada):
    # (Descrição, Bruto XP, Líquido XP, Escritório, Comissão, Total)
    query = db.session.query(
                            cls.produto,
                            db.func.sum(cls.aportes_receita),
                            db.func.sum(cls.receita_bruta_total),
                            db.func.sum(cls.receita_liquida_total),
                            db.literal(assessor.comissao_rv),
                            db.func.sum(cls.receita_liquida_total) * db.literal(assessor.comissao_rv)
    ).group_by(
                            cls.produto
    ).filter(
                            cls.tipo.in_(cls.RECEITAS),
                            cls.codigo_a == assessor.codigo_a,
                            cls.mes_de_entrada == mes_de_entrada,
        )

    query = list(query)
    if len(query) == 0:
      return [('-', 0, 0, 0, 0, 0)]

    return query

  @classmethod
  def descontos(cls, assessor, mes_de_entrada):
    query = db.session.query(
                            cls.produto,
                            db.func.sum(cls.receita_liquida_total)
    ).group_by(
                            cls.produto
    ).filter(
                            cls.produto.in_(cls.DESCONTOS),
                            cls.email == assessor.email,
                            cls.mes_de_entrada == mes_de_entrada,
        )

    query = list(query)
    if len(query) == 0:
      return [('-', 0)]

    return query

  filters = {
    'receita_bruta_total': 'currency',
    'ir_sobre_receita_bruta': 'currency',
    'receita_liquida_total': 'currency'
  }

  RECEITAS = [
    "Adiantamento Previdência",
    "Estorno Adiantamento",
    "Previdência"
  ]

  DESCONTOS = [
  ]