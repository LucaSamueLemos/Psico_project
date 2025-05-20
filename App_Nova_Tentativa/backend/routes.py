# backend/routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Paciente, RegistroEmocao # Importe RegistroEmocao aqui
from . import db # Ainda precisamos do db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login realizado com sucesso!', category='success')
            login_user(user, remember=True)
            if user.tipo == 'paciente':
                return redirect(url_for('routes.paciente'))
            elif user.tipo == 'psicologo':
                return redirect(url_for('routes.psicologo'))
        else:
            flash('Email ou senha incorretos.', category='error')

    return render_template('index.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', category='info')
    return redirect(url_for('routes.login'))

@routes.route('/paciente')
@login_required
def paciente():
    if current_user.tipo != 'paciente':
        flash('Acesso não autorizado.', category='error')
        return redirect(url_for('routes.login'))
    return render_template('paciente.html')

@routes.route('/registrar_emocao', methods=['POST'])
@login_required
def registrar_emocao():
    if current_user.tipo == 'paciente':
        emocao = request.form.get('emocao')
        nova_emocao = RegistroEmocao(emocao=emocao, paciente_id=current_user.id)
        db.session.add(nova_emocao)
        db.session.commit()
        flash('Emoção registrada com sucesso!', category='success')
    else:
        flash('Acesso não autorizado.', category='error')
    return redirect(url_for('routes.paciente'))

@routes.route('/psicologo')
@login_required
def psicologo():
    if current_user.tipo != 'psicologo':
        flash('Acesso não autorizado.', category='error')
        return redirect(url_for('routes.login'))
    pacientes = Paciente.query.filter_by(psicologo_id=current_user.id).all()
    return render_template('psicologo.html', pacientes=pacientes)

# As outras rotas para registrar emoções, questionários, etc., virão aqui.