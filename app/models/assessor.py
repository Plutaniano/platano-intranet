from typing import Union, Dict, Set
from flask import current_app
from ..models import *
from flask_login import UserMixin
from sqlalchemy import Integer, String, Float, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base
import datetime
from typing import Dict


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

    def resumo(self, mes_de_entrada: datetime.date):
        '''\
        Retorna um dicionário contendo todas as informações necessárias para apresentar
        a página resumo para o assessor.\
        '''
        t = current_app.config['TABELAS_COM_RECEITA']

        resumo = {
            'Investimentos':         { 'Receita': (receita := t['investimentos'].receita_do_escritorio(self.codigo_a, mes_de_entrada)),
                                       'Descontos': (descontos := t['investimentos'].descontos(self.codigo_a, mes_de_entrada)),
                                       'Comissão': self.comissao_rv,
                                       'Assessor': int((receita['Escritório'] - descontos) * self.comissao_rv)
                                     },

            'Previdencia':           { 'Receita': (receita := t['previdencia'].receita_do_escritorio(self.codigo_a, mes_de_entrada)),
                                       'Descontos': (descontos := t['previdencia'].descontos(self.codigo_a, mes_de_entrada)),
                                       'Comissão': self.comissao_previdencia,
                                       'Assessor': int((receita['Escritório'] - descontos) * self.comissao_previdencia)
                                     },

            'Banco XP':              { 'Receita': (receita := t['banco_xp'].receita_do_escritorio(self.codigo_a, mes_de_entrada)),
                                       'Comissão': self.comissao_bancoxp,
                                       'Assessor': int(receita['Escritório'] * self.comissao_bancoxp)
                                     },

            'Cambio':                { 'Receita': (receita := t['cambio'].receita_do_escritorio(self.codigo_a, mes_de_entrada)),
                                       'Comissão': self.comissao_cambio,
                                       'Assessor': int(receita['Escritório'] * self.comissao_cambio)
                                     },

            'Co-corretagem':         { 'Receita': (receita := t['cocorretagem'].receita_do_escritorio(self.codigo_a, mes_de_entrada)),
                                       'Comissão': 1,
                                       'Assessor': int(receita['Escritório'] * 1)
                                     },
        }

        resumo['Total Bruto'] = resumo['Investimentos']['Assessor']\
                          + resumo['Previdencia']['Assessor']\
                          + resumo['Banco XP']['Assessor']\
                          + resumo['Cambio']['Assessor']\
                          + resumo['Co-corretagem']['Assessor']

        resumo['Impostos'] = resumo['Total Bruto'] * 0.2
        resumo['Total Líquido'] = resumo['Total Bruto'] - resumo['Impostos']

        return resumo

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
