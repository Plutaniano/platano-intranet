import datetime
import os

from flask import Blueprint, render_template, request, url_for, redirect, Response, flash
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import secure_filename

from . import login_manager
from intranet.forms import ForgotForm, QueryForm, LoginForm, UploadForm, ResumoForm, OutroForm
from . import app
from .models import *
from .utils import query_to_csv
from .parser import parse_excel

views = Blueprint('views', __name__)

@app.template_filter()
def fmt(value, filter):
    if filter == 'currency':
        if value in [0, None]:
            return '-'

        value *= 0.01
        t = "{0:,.2f}".format(value)
        t = t.replace(',', '*')
        t = t.replace('.', ',')
        return t.replace('*', '.')

    if filter == 'none_filter':
        return value or '-'

    if filter == 'percent':
        value *= 100
        return "{0:,.2f}%".format(value)

    if filter == 'date':
        return value.strftime("%d/%m/%Y")

@app.template_filter()
def jinja_zip(*args):
    return zip(*args)

@login_manager.user_loader
def load_user(id=None, **kw):
    if id:
        return Usuario.query.get(id)
    else:
        return db.session.query(Usuario).filter_by(**kw).first()
    
    
# ------------------------
#        user pages
# ------------------------
@views.route('/')
def home():
    return render_template('pages/home.html')

@views.route('/sobre')
def sobre():
    return render_template('pages/sobre.html')

@views.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@views.route('/consulta', methods=['GET', 'POST'])
@login_required
def consulta():
    if current_user.is_admin:
        assessores = list(db.session.query(Usuario))
    else:
        assessores = [current_user]

    anos_meses = set()
    for q in TABELAS_COM_RECEITA.values():
        query = db.session.query(q.mes_de_entrada)
        for q in query:
            q = q[0]
            anos_meses.add(q.strftime('%Y/%m'))
    
    form = QueryForm()
    for i in anos_meses:
        form.ano_mes.choices.append(i)

    if request.method == 'GET':
        return render_template('pages/consulta.html', assessores=assessores, anos_meses=anos_meses, form=form)

    if request.method == 'POST':
        assessor = load_user(id=form.id.data)
        ano, mes = map(int, request.form.get('ano_mes').split('/'))
        ano_mes = datetime.date(ano, mes, 1)
        tabela = TABELAS_COM_RECEITA[request.form.get('tabela')]

        query = tabela.consulta(assessor, ano_mes)


        if request.form.get('action')== 'Exportar':
            text = query_to_csv(data, d[tabela], assessor.codigo_a)
            return Response(text,
                            mimetype="text/csv",
                            headers={"Content-disposition": "attachment; filename=tabela.csv"})

        return render_template('pages/consulta.html', query=query, form=form, tabela=tabela)

@views.route('/resumo', methods=['GET', 'POST'])
@login_required
def resumo():
    form = ResumoForm()

    # lista de assessores
    if current_user.is_admin:
        assessores = list(db.session.query(Usuario))
    else:
        assessores = [current_user]

    for i in assessores:
        t = (i.id, str(i.nome))
        form.usuarios.choices.append(t)

    # lista de anos_meses
    anos_meses = set()
    for q in TABELAS_COM_RECEITA.values():
        query = db.session.query(q.mes_de_entrada).distinct()
        for q in query:
            anos_meses.add(q[0].strftime('%Y/%m'))    

    for i in anos_meses:
        form.ano_mes.choices.append(i)



    if request.method == 'POST':
        assessor = load_user(id=form.usuarios.data)
        ano, mes = map(int, form.ano_mes.data.split('/'))
        ano_mes = datetime.date(ano, mes, 1)
        
        receita = assessor.resumo(ano_mes)
        descontos = assessor.descontos(ano_mes)

        total = 0
        for segmento in receita:
            for produto in receita[segmento]:
                total += produto[5]

        total_receitas = total
        impostos = total_receitas * -0.2

        for segmento in descontos:
            for produto in descontos[segmento]:
                total += produto[1]
        
        total_descontos = total - total_receitas
        total += impostos

        return render_template('pages/resumo.html', form=form, receita=receita, descontos=descontos, total_receitas=total_receitas, impostos=impostos, total_descontos=total_descontos, total=total)
    
    if request.method == 'GET':
        return render_template('pages/resumo.html', form=form)



# ------------------------
#      admin pages
# ------------------------
@views.route('/inserir_tabela')
@login_required
def inserir_tabela():
    if not current_user.is_admin:
        return 'Não autorizado'
        
    return render_template('pages/inserir_tabela.html', uploadform=UploadForm())


@views.route('/upload', methods=['POST'])
@login_required
def upload():
    if not current_user.is_admin:
        return 'Não autorizado'

    form = UploadForm()
    f = form.planilha.data
    date = form.mes_de_entrada.data
    filename = secure_filename(f.filename)
    path = 'C:\\Windows\\Temp\\' if os.name == 'nt' else '/tmp/'
    f.save(path + filename)
    results = parse_excel(path + filename, date)
    results = ', '.join(i[0] for i in results if i[1])
    flash('Tabelas processadas: ' + results)
    return redirect(url_for('views.inserir_tabela'))


@views.route('/adicionar_outros', methods=['GET', 'POST'])
@login_required
def adicionar_outros():
    if not current_user.is_admin:
        return 'Não autorizado'

    form = OutroForm()
    
    if request.method == 'GET':
        return render_template('pages/adicionar_outros.html', form=form)


    if request.method == 'POST':
        id = form.id.data
        descricao = form.descricao.data
        valor = int(100 * form.valor.data)
        ano_mes = form.mes_de_entrada.data

        entry = Outros(id=id, descricao=descricao, valor=valor, mes_de_entrada=ano_mes)
        db.session.add(entry)
        db.session.commit()

        flash('Adicionado com sucesso.')
        return render_template('pages/adicionar_outros.html', form=form)


@views.route('/comissoes')
@login_required
def comissoes():
    if not current_user.is_admin:
        return 'Não autorizado'

    query = db.session.query(
        Usuario.id,
        Usuario.nome,
        Usuario.email,
        Usuario.segmento,
        Usuario.filial,
        Usuario.fixo,
        Usuario.comissao_rv,
        Usuario.comissao_alocacao,
        Usuario.comissao_previdencia,
        Usuario.comissao_seguros,
        Usuario.comissao_bancoxp,
        Usuario.comissao_cambio
    )

    filters = Usuario.filters
    return render_template('pages/comissoes.html', query=query, filters=filters)


# ------------------------
#           auth
# ------------------------
@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(email=form.email.data)

        if user is None or user.password != form.password.data:
            flash('Credenciais invalidas')
            return redirect(url_for('views.login'))

        login_user(user)                                        # TODO: Adicionar remember_me
        return redirect(url_for('views.home'))

    return render_template('forms/login.html', form=form)

@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))