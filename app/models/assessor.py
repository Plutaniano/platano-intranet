from typing import Union, Dict
from flask import current_app
from ..models import *
from flask_login import UserMixin
from sqlalchemy import Integer, String, Float, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base
from . import db
import datetime


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

    def resumo(self, mes_de_entrada: datetime.date) -> Dict:
        '''\
        Retorna um dicionário contendo todas as informações necessárias para apresentar
        a página resumo para o assessor.\
        '''
        tabelas = current_app.config['TABELAS_COM_RECEITA']

        d = {
            'receita_total': 0
        }

        for tabela in tabelas:
            d[tabela] = tabela.receita_do_escritorio(self.codigo_a, mes_de_entrada)
            d['receita_total'] += d[tabela]

        return d

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
