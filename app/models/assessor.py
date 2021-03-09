import datetime

from flask import current_app
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

    def meses_com_entrada(self):
        tabelas = current_app.config['TABELAS_COM_RECEITA']
        meses_com_entrada =set()

        for tabela in tabelas.values():
            q = db.session.query(tabela.mes_de_entrada).filter_by(codigo_a = self.codigo_a).distinct()
            for i in q:
                meses_com_entrada.add(i.mes_de_entrada)
        
        return meses_com_entrada

    def resumo(self, mes_de_entrada: datetime.date):
        t = current_app.config['TABELAS_COM_RECEITA']
        
        resumo = {
            'Investimentos': list(((*i, self.comissao_rv, i[3] * self.comissao_rv) for i in t['investimentos'].receitas(self, mes_de_entrada))),

            'Alocação': list(((*i, self.comissao_alocacao, i[3] * self.comissao_alocacao) for i in t['investimentos'].receitas_alocacao(self, mes_de_entrada))),

            'Prêvidencia': list(((*i, self.comissao_previdencia, i[3] * self.comissao_previdencia) for i in t['previdencia'].receitas(self, mes_de_entrada))),

            'Banco XP': list(((i[0], 0, i[1], i[2], self.comissao_bancoxp, i[2] * self.comissao_bancoxp) for i in t['banco_xp'].receitas(self, mes_de_entrada))),

            'Cambio': list(((i[0], 0, 0, i[1], self.comissao_cambio, i[1] * self.comissao_cambio) for i in t['cambio'].receitas(self, mes_de_entrada))),

            'Co-corretagem': list(((*i, 1, i[3] * 1) for i in t['cocorretagem'].receitas(self, mes_de_entrada)))
        }

        return resumo

    def descontos(self, mes_de_entrada: datetime.date):
        t = current_app.config['TABELAS_COM_RECEITA']
        
        descontos = {
            'Descontos Prêvidencia': list((*i,) for i in t['previdencia'].descontos(self, mes_de_entrada)),

            'Descontos Investimentos': list((*i,) for i in t['investimentos'].descontos(self, mes_de_entrada))
        }

        return descontos

        

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

    def get_id(self):
        '''\
        Função para a utilização da biblioteca flask_login\
        '''
        return self.codigo_a

    def __repr__(self):
        user_type = 'ADMIN' if self.is_admin else 'USER'
        return f"<Assessor [{user_type}] A{self.codigo_a}:{self.nome}>"
