import datetime

from flask_login import UserMixin


from .investimentos import Investimentos
from .previdencia import Previdencia
from .cambio import Cambio
from .cocorretagem import CoCorretagem
from .outros import Outros
from .bancoxp import BancoXP
from . import db
from intranet import app

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    __displayname__ = 'Usuários'

    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('Nome', db.String(100))
    password = db.Column('Senha', db.String(30))
    email = db.Column('Email', db.String(120))
    obs = db.Column('Observações', db.String(120))
    is_admin = db.Column('admin?', db.Boolean,)
    segmento = db.Column('Segmento', db.String(20))
    filial = db.Column('Filial', db.String(20))
    fixo = db.Column('Fixo', db.Integer)
    
    codigo_a = db.Column('Código A', db.Integer)
    clientes = db.relationship('Cliente', backref='assessor')

    comissao_rv = db.Column('Comissão RV', db.Float, default=0.3)
    comissao_alocacao = db.Column('Comissão Alocação', db.Float, default=0.45)
    comissao_previdencia = db.Column('Comissão Previdência', db.Float, default=0.3)
    comissao_seguros = db.Column('Comissão Seguros', db.Float, default=0.3)
    comissao_bancoxp = db.Column('Comissão Banco XP', db.Float, default=0.3)
    comissao_cambio = db.Column('Comissão Câmbio', db.Float, default=0.3)


    def meses_com_entrada(self):
        tabelas = app.config['TABELAS_COM_RECEITA']
        meses_com_entrada = set()

        for tabela in tabelas.values():
            q = db.session.query(tabela.mes_de_entrada).filter_by(codigo_a = self.codigo_a).distinct()
            for i in q:
                meses_com_entrada.add(i.mes_de_entrada)
        
        return meses_com_entrada

    def resumo(self, mes_de_entrada):
        
        resumo = {
            'Renda Variável': Investimentos.receitas_rv(self, mes_de_entrada),

            'Alocação': Investimentos.receitas_alocacao(self, mes_de_entrada),

            'Prêvidencia': Previdencia.receitas(self, mes_de_entrada),

            'Banco XP': BancoXP.receitas(self, mes_de_entrada),

            'Cambio': Cambio.receitas(self, mes_de_entrada),

            'Co-corretagem': CoCorretagem.receitas(self, mes_de_entrada),

            'Outros': Outros.receitas(self, mes_de_entrada)
        }

        return resumo

    def descontos(self, mes_de_entrada):

        descontos = {
            'Descontos Investimentos': Investimentos.descontos(self, mes_de_entrada),

            'Descontos Outros': Outros.descontos(self, mes_de_entrada)
        }

        return descontos

    def get_id(self):
        '''\
        Função para a utilização da biblioteca flask_login\
        '''
        return self.id  

    def __repr__(self):
        return f"<User [{self.segmento}] ID[{self.id}]:{self.nome}>"
