from flask import Blueprint, render_template, request, url_for, redirect, Response, flash
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import secure_filename
from . import login_manager
from .forms import ForgotForm, QueryForm, LoginForm, RegisterForm, UploadForm
import datetime
from sqlalchemy.orm import sessionmaker
from . import app
import os
from sqlalchemy import extract
from .models import db, Assessor, Investimentos, IncentivoPrevidencia, BancoXP, Previdencia, Cambio, CoCorretagem
from .utils import query_to_csv
import datedelta
from .parser import parse_excel

views = Blueprint('views', __name__)

@login_manager.user_loader
def load_user(id):
    user = db.session.query(Assessor).filter_by(codigo_a=id).first()
    return user
    
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
        assessores = list(db.session.query(Assessor))
    else:
        assessores = [current_user]
    
    queries = [
            Investimentos,
            Previdencia,
            CoCorretagem,
            IncentivoPrevidencia,
            Cambio,
            BancoXP
        ]

    anos_meses = set()
    for q in queries:
        query = db.session.query(q.mes_de_entrada)
        for q in query:
            q = q[0]
            anos_meses.add(q.strftime('%Y/%m'))
    
    form = QueryForm(request.form)
    for i in anos_meses:
        form.ano_mes.choices.append(i)

    for i in assessores:
        t = (i.codigo_a, 'A' + str(i.codigo_a) + ' - ' + str(i.nome))
        form.assessores.choices.append(t)

    if request.method == 'GET':
        return render_template('pages/consulta.html', assessores=assessores, anos_meses=anos_meses, form=form)

    if request.method == 'POST':
        assessor = load_user(request.form.get('assessores'))
        ano = int(request.form.get('ano_mes').split('/')[0])
        mes = int(request.form.get('ano_mes').split('/')[1])
        ano_mes = datetime.date(ano, mes, 1)
        tabela = request.form.get('tabela')

        d = {
            'investimentos': Investimentos,
            'previdencia': Previdencia,
            'co_corretagem': CoCorretagem,
            'incentivo_previdencia': IncentivoPrevidencia,
            'bancoXP': BancoXP,
            'cambio': Cambio
        }

        data = db.session                                               \
                    .query(*(i[0] for i in d[tabela].showable_columns))\
                    .filter(
                        d[tabela].codigo_a == assessor.codigo_a,
                        d[tabela].mes_de_entrada == ano_mes
                        )

        if request.form.get('action')== 'Exportar':
            text = query_to_csv(data, d[tabela], assessor.codigo_a)
            return Response(text, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=tabela.csv"})

        return render_template('pages/consulta.html', assessores=assessores, anos_meses=anos_meses, data=data, form=form, tabela=d[tabela])



# ------------------------
#      admin pages
# ------------------------
@views.route('/admin')
@login_required
def admin():
    return render_template('pages/admin.html', uploadform=UploadForm())



@views.route('/upload', methods=['POST'])
@login_required
def upload():
    form = UploadForm()
    f = form.planilha.data
    date = form.mes_de_entrada.data
    filename = secure_filename(f.filename)
    f.save('/tmp/' + filename)
    results = parse_excel('/tmp/' + filename, date)
    results = ', '.join(i[0] for i in results if i[1])
    flash('Tabelas processadas: ' + results)
    return redirect(url_for('views.admin'))


@views.route('/assessores')
@login_required
def assessores():
    assessores = db.session.query(Assessor)
    return render_template('pages/assessores.html', assessores=assessores)


# ------------------------
#           auth
# ------------------------
@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = load_user(form.codigo_a.data)
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