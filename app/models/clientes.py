from . import *

class Cliente(db.Model):
  __tablename__ = 'clientes'
  __displayname__ = 'Clientes'
  
  id = Column('Código do Cliente', Integer, primary_key=True)
  comissao_rv = Column('Comissão RV', Float)
  codigo_a = Column('Codigo do Assessor', Integer, ForeignKey('usuarios.Código A'))
  comissao_alocacao = Column('Comissão Alocação', Float)
  comissao_previdencia = Column('Comissão Previdência', Float)
  comissao_seguros = Column('Comissão Seguros', Float)
  comissao_bancoxp = Column('Comissão Banco XP', Float)
  comissao_cambio = Column('Comissão Câmbio', Float)