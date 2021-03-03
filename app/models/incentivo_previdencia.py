from sqlalchemy import Integer, String, Float, Boolean, Date, Column
from . import db, Assessor
from typing import Dict


class IncentivoPrevidencia(db.Model):
  __tablename__ = 'incentivo_previdencia'
  __displayname__ = 'Incentivo Previdência'
  id = Column('ENTRY ID', Integer, primary_key=True)
  mes_de_entrada = Column('MES DE ENTRADA', Date)
  comissionamento = Column('COMISSIONAMENTO', String(21), default='incentivo_previdencia')

  mes_referencia = Column('Mês de Referência', Date)
  status_docusign = Column('Status Docusign', Boolean)
  codigo_escritorio = Column('Código do Escritório', Integer)
  escritorio = Column('Escritório', String(60))
  codigo_a = Column('Código A', Integer)
  codigo_cliente  = Column('Código do Cliente', Integer)
  certificado = Column('Certificado - Fundo', String(60))
  movimentacao_cliente = Column('Movimentação Cliente', Integer)
  adiantamento_previdencia = Column('Adiantamento da Previdência', Integer)

  @classmethod
  def receita_do_escritorio(cls, codigo_a: int, mes_de_entrada: Date) -> Dict:
    f'''\
      Retorna a receita gerada no seguimento `{cls.__displayname__}` para o escritório pelo `assessor` durante o `mes_de_entrada`.
      Não inclui cálculos de comissão.\
    '''
    receita = {}

    query = db.session.query(cls.adiantamento_previdencia).filter_by(codigo_a = codigo_a, mes_de_entrada=mes_de_entrada)
    
    receita['Bruto XP'] = 0
    receita['Líquido XP'] = 0
    receita['Escritório'] = sum(i[0] for i in query)

    return receita

  showable_columns = [
    (codigo_cliente, lambda x: x, ''),
    (certificado, lambda x: x, ''),
    (movimentacao_cliente, lambda x: '%.2f' % (0.01 * x), '(R$)'),
    (adiantamento_previdencia, lambda x: '%.2f' % (x * 0.01), '(R$)')
  ]
