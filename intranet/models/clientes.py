from . import db

class Cliente(db.Model):
  __tablename__ = 'clientes'
  __displayname__ = 'Clientes'
  
  id= db.Column('Código do Cliente', db.Integer, primary_key=True)
  comissao_rv= db.Column('Comissão RV', db.Float)
  codigo_a= db.Column('Codigo do Assessor', db.Integer, db.ForeignKey('usuarios.Código A'))
  comissao_alocacao= db.Column('Comissão Alocação', db.Float)
  comissao_previdencia= db.Column('Comissão Previdência', db.Float)
  comissao_seguros= db.Column('Comissão Seguros', db.Float)
  comissao_bancoxp= db.Column('Comissão Banco XP', db.Float)
  comissao_cambio= db.Column('Comissão Câmbio', db.Float)