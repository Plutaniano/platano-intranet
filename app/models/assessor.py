from typing import Union, Dict, Set
from flask import current_app
from ..models import *
from flask_login import UserMixin
from sqlalchemy import Integer, String, Float, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base
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

    def meses_com_entrada(self) -> Set[datetime.date]:
        tabelas = current_app.config['TABELAS_COM_RECEITA']
        meses_com_entrada =set()

        for tabela in tabelas.values():
            q = db.session.query(tabela.mes_de_entrada).filter_by(codigo_a = self.codigo_a).distinct()
            for i in q:
                meses_com_entrada.add(i.mes_de_entrada)
        
        return meses_com_entrada

    def resumo(self, mes_de_entrada: datetime.date) -> Dict[str, int]:
        '''\
        Retorna um dicionário contendo todas as informações necessárias para apresentar
        a página resumo para o assessor.\
        '''
        t = current_app.config['TABELAS_COM_RECEITA']
        impostos = current_app.config['IMPOSTOS']

        d = {
            'Investimentos': t['investimentos'].receita_do_escritorio(self.codigo_a, mes_de_entrada),
            'Previdencia': t['previdencia'].receita_do_escritorio(self.codigo_a, mes_de_entrada),
            'Banco XP': t['banco_xp'].receita_do_escritorio(self.codigo_a, mes_de_entrada),
            'Incentivo Previdencia': t['incentivo_previdencia'].receita_do_escritorio(self.codigo_a, mes_de_entrada),
            'Cambio': t['cambio'].receita_do_escritorio(self.codigo_a, mes_de_entrada),
            'Co-corretagem': t['cocorretagem'].receita_do_escritorio(self.codigo_a, mes_de_entrada)
        }

        d['Receita Bruta'] = sum(d.values())

        liquida = d['Receita Bruta']

        for nome, taxa in impostos.items():
            d[nome] = d['Receita Bruta'] * taxa * -1
            liquida  += d[nome]
        
        d['Receita Liquida'] = liquida

        for key, value in d.items():
            value = float(value * 0.01)
            d[key] =  value

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
