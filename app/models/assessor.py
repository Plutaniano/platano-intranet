from flask_login import UserMixin
from sqlalchemy import Integer, String, Float, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base
from . import db


class Assessor(UserMixin, db.Model):
    __tablename__ = 'assessores'
    __displayname__ = 'Assessores'
    codigo_a = Column('Código A', Integer, primary_key=True, unique=True)
    nome = Column('Nome', String(50))
    password = Column('Senha', String(30))
    email = Column('Email', String(120), unique=True)
    is_admin = Column('admin?', Boolean, default=False)
    comissao_rv = Column('Comissão RV', Float, default=0.0)
    comissao_alocacao = Column('Comissão Alocação', Float, default=0.0)
    comissao_previdencia = Column('Comissão Previdência', Float, default=0.0)
    comissao_seguros = Column('Comissão Seguros', Float, default=0.0)
    comissao_bancoxp = Column('Comissão Banco XP', Float, default=0.0)
    comissao_cambio = Column('Comissão Câmbio', Float, default=0.0)
    obs = Column('Observações', String(120), default=None)

    def get_id(self):
        return self.codigo_a

    def __repr__(self):
        user_type = 'ADMIN' if self.is_admin else 'USER'
        return f"<Assessor [{user_type}] A{self.codigo_a}:{self.nome}>"

    showable_columns = [
    (codigo_a, lambda x: 'A' + str(x), ''),
    (nome, lambda x: x, ''),
    (comissao_rv, lambda x: x, ''),
    (comissao_alocacao, lambda x: x, ''),
    (comissao_previdencia, lambda x: x, ''),
    (comissao_seguros, lambda x: x, ''),
    (comissao_bancoxp, lambda x: x, ''),
    (comissao_cambio, lambda x: x, ''),
  ]
