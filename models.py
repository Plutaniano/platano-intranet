# coding=utf-8
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(app)

class Assessor(UserMixin, db.Model):
  codigo_assessor = db.Column(db.Integer, primary_key=True, unique=True)
  nome = db.Column(db.String(50))
  password = db.Column(db.String(30))
  email = db.Column(db.String(120), unique=True)
  is_admin = db.Column(db.Boolean, default=False)
  comissao_rv = db.Column(db.Float, default=0.0)
  comissao_alocacao = db.Column(db.Float, default=0.0)
  comissao_previdencia = db.Column(db.Float, default=0.0)
  comissao_seguros = db.Column(db.Float, default=0.0)
  comissao_bancoxp = db.Column(db.Float, default=0.0)
  comissao_cambio = db.Column(db.Float, default=0.0)
  obs = db.Column(db.String(120), default=None)

  def get_id(self):
    return self.codigo_assessor

 # def __repr__(self):
 #   return f"<Assessor {'[ADMIN]' if self.is_admin else ''} A{self.assessor_codigo}:{self.nome}>"

class Investimentos(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ano_mes = db.Column(db.Date)
  
  classificacao = db.Column(db.String(20))
  produto = db.Column(db.String(50))
  nivel1 = db.Column(db.String(200))
  nivel2 = db.Column(db.String(50))
  nivel3 = db.Column(db.String(50))
  cliente = db.Column(db.Integer)
  master = db.Column(db.Integer)
  data = db.Column(db.Date)
  receita_bruta = db.Column(db.Integer)
  receita_liquida = db.Column(db.Integer)
  comissao_escritorio_porcento = db.Column(db.Float) 
  comissao_escritorio = db.Column(db.Integer)
  
  codigo_assessor = db.Column(db.Integer)
  assessor_direto_comissao_porcento = db.Column(db.Integer)
  assessor_direto_comissao = db.Column(db.Integer)

  assessor_indireto1_codigo = db.Column(db.Integer)
  assessor_indireto1_comissao_porcento = db.Column(db.Integer)
  assessor_indireto1_comissao = db.Column(db.Integer)

  assessor_indireto2_codigo = db.Column(db.Integer)
  assessor_indireto2_comissao_porcento = db.Column(db.Integer)
  assessor_indireto2_comissao = db.Column(db.Integer)

  assessor_indireto3_codigo = db.Column(db.Integer)
  assessor_indireto3_comissao_porcento = db.Column(db.Integer)
  assessor_indireto3_comissao = db.Column(db.Integer)


class Previdencia(db.Model):
  # Dados Cliente
  id = db.Column(db.Integer, primary_key=True)
  ano_mes = db.Column(db.Date)

  tipo = db.Column(db.String(50))
  competencia = db.Column(db.Date)
  parceiro = db.Column(db.String(60))
  codigo_assessor = db.Column(db.Integer)
  certificado = db.Column(db.Integer)
  cpf = db.Column(db.String(11))
  codigo_cliente = db.Column(db.Integer)
  up = db.Column(db.String(60))
  
  # Dados do produto
  seguradora = db.Column(db.String(30))
  produto = db.Column(db.String(120))
  data_emissao = db.Column(db.Date)
  reserva = db.Column(db.Integer)
  tx_adm = db.Column(db.Float)

  # TAF
  taf_base = db.Column(db.Integer)
  taf_repasse_porcento = db.Column(db.Float)
  taf_receita = db.Column(db.Integer)
  
  # 1a Aplicacao Mensal
  primeira_aplicacao_mensal_base = db.Column(db.Integer)
  primeira_aplicacao_mensal_repasse = db.Column(db.Float)
  primeira_aplicacao_mensal_receita = db.Column(db.Integer)


  # Aportes/Premio
  aportes_base = db.Column(db.Integer)
  aportes_repasse_porcento = db.Column(db.Float)
  aportes_receita = db.Column(db.Integer)
  
  # Portabilidade
  portabilidade_base = db.Column(db.Integer)
  portabilidade_repasse_porcento = db.Column(db.Integer)
  portabilidade_receita = db.Column(db.Integer)

  # Receita
  receita_bruta_total = db.Column(db.Integer)
  ir_sobre_receita_bruta = db.Column(db.Float)
  receita_liquida_total = db.Column(db.Integer)
  obs = db.Column(db.String(120))



class CoCorretagem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ano_mes = db.Column(db.Date)

  tipo = db.Column(db.String(30))
  competencia = db.Column(db.Date)
  parceiro = db.Column(db.String(60))
  codigo_assessor = db.Column(db.Integer)

  certificado = db.Column(db.Integer)
  cpf = db.Column(db.String(11))
  codigo_cliente = db.Column(db.Integer)
  nome_cliente = db.Column(db.String(120))

  seguradora = db.Column(db.String(30))
  produto = db.Column(db.String(60))
  data_emissao = db.Column(db.Date)
  reserva = db.Column(db.Integer)
  tx_adm = db.Column(db.Integer)

  taf_base = db.Column(db.Integer)
  taf_repasse_porcento = db.Column(db.Float)
  taf_receita = db.Column(db.Integer)

  primeira_aplicacao_mensal_base = db.Column(db.Integer)
  primeira_aplicacao_mensal_repasse = db.Column(db.Float)
  primeira_aplicacao_mensal_receita = db.Column(db.Integer)

  aportes_base = db.Column(db.Integer)
  aportes_repasse_porcento = db.Column(db.Float)
  aportes_receita = db.Column(db.Integer)

  portabilidade_base = db.Column(db.Integer)
  portabilidade_repasse_porcento = db.Column(db.Float)
  portabilidade_receita = db.Column(db.Integer)

  receita_total = db.Column(db.Integer)
  obs = db.Column(db.String(100))


class IncentivoPrevidencia(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ano_mes = db.Column(db.Date)

  mes_referencia = db.Column(db.Integer)
  status_docusign = db.Column(db.Boolean)
  codigo_escritorio = db.Column(db.Integer)
  escritorio = db.Column(db.String(60))
  codigo_assessor = db.Column(db.Integer)
  codigo_cliente  = db.Column(db.Integer)
  certificado = db.Column(db.String(60))
  movimentacao_cliente = db.Column(db.Integer)
  adiantamento_previdencia = db.Column(db.Integer)
  

class BancoXP(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ano_mes = db.Column(db.Date)

  competencia = db.Column(db.Date)
  codigo_escritorio = db.Column(db.Integer)
  parceiro = db.Column(db.String(60))
  codigo_assessor = db.Column(db.Integer)
  operacao = db.Column(db.Integer)
  codigo_cliente = db.Column(db.Integer)
  produto = db.Column(db.String(60))
  data_contratacao = db.Column(db.Date)
  data_vencimento = db.Column(db.Date)
  valor_contratado = db.Column(db.Integer)
  juros_aa = db.Column(db.Integer)
  comissao_escritorio_porcento_aa = db.Column(db.Integer)
  comissao_atualizada_acumulada = db.Column(db.Integer)
  deducoes = db.Column(db.Float)
  total_receita = db.Column(db.Integer)

class Cambio(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ano_mes = db.Column(db.Date)

  codigo_cliente = db.Column(db.Integer)
  tipo = db.Column(db.String(20))
  data = db.Column(db.Date)
  moeda = db.Column(db.String(5))
  volume = db.Column(db.Integer)
  receita = db.Column(db.Integer)
  taxa_cliente = db.Column(db.Float)
  taxa_base = db.Column(db.Float)
  spread_aplicado = db.Column(db.Float)
  codigo_assessor = db.Column(db.Integer)



if __name__ == '__main__':
  import datetime
  from openpyxl import load_workbook
  from parse import parse_investimentos, parse_previdencia, parse_co_corretagem, parse_excel, parse_cambio
  
  db.create_all()
  wb = load_workbook('sistema.xlsx')
  date = datetime.date(2000,1,1)
