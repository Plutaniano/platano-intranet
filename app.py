from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from forms import *
from validate import *
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)

from models import *

@login_manager.user_loader
def load_user(id):
    user = db.session.query(Assessor).filter_by(id=id).first()
    return user

# ------------------------
#        user pages
# ------------------------
@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/sobre')
def sobre():
    return render_template('pages/sobre.html')

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/consulta', methods=['GET', 'POST'])
@login_required
def consulta():
    if current_user.is_admin:
        assessores = list(db.session.query(Assessor))
    else:
        assessores = [current_user]

    form = QueryForm(request.form)

    anos_meses = list(db.session.query(Investimentos.ano_mes).distinct())
    for i in anos_meses:
        s = i.ano_mes.strftime('%Y/%m')
        form.ano_mes.choices.append((s, s))
    
    for i in assessores:
        t = (i.id, 'A' + str(i.id) + ' - ' + i.nome)
        form.assessores.choices.append(t)

    if request.method == 'GET':
        return render_template('pages/consulta.html', assessores=assessores, anos_meses=anos_meses, form=form)

    if request.method == 'POST':

        assessor = load_user(request.form.get('assessores'))
        ano = int(request.form.get('ano_mes').split('/')[0])
        mes = int(request.form.get('ano_mes').split('/')[1])
        ano_mes = date(ano, mes, 1)
        tabela = request.form.get('tabela')

        d = {
            'investimentos': Investimentos,
            'previdencia': Previdencia,
            'co_corretagem': CoCorretagem,
            'incentivo_previdencia': IncentivoPrevidencia,
            'bancoXP': BancoXP
        }

        data = db.session.query(d[tabela]).filter_by(codigo_assessor=assessor.id, ano_mes=ano_mes)
        return render_template('pages/consulta.html', assessores=assessores, anos_meses=anos_meses, data=data, form=form, tabela=tabela)



# ------------------------
#      admin pages
# ------------------------
@app.route('/admin')
@login_required
def admin():
    return render_template('pages/admin.html', registerform=RegisterForm(request.form))

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    return 'a'

@app.route('/adicionarassessor', methods=['POST'])
@login_required
def adicionarassessor():
    form = RegisterForm(request.form)
    db.session.add(Assessor(id=form.id.data, nome=form.name.data, email=form.email.data))
    db.session.commit()
    flash('Assessor adicionado com sucesso.')
    return redirect(url_for('admin'))


@app.route('/assessores')
@login_required
def assessores():
    assessores = db.session.query(Assessor)
    return render_template('pages/comissoes.html', assessores=assessores)


# ------------------------
#           auth
# ------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = load_user(form.id.data)
        if user is None or user.password != form.password.data:
            flash('Credenciais inválidas')
            return redirect(url_for('login'))
        login_user(user)                                        # TODO: Adicionar remember_me
        return redirect(url_for('home'))
    return render_template('forms/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
