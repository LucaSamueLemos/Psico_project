# backend/models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    tipo = db.Column(db.String(50)) # 'paciente' ou 'psicologo'
    pacientes = db.relationship('Paciente', backref='psicologo', foreign_keys='Paciente.psicologo_id')

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    psicologo_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registros_emocoes = db.relationship('RegistroEmocao', backref='paciente')
    respostas_questionario = db.relationship('RespostaQuestionario', backref='paciente')
    consultas = db.relationship('Consulta', backref='paciente')

class RegistroEmocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emocao = db.Column(db.String(150))
    data_registro = db.Column(db.DateTime(timezone=True), default=func.now())
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class RespostaQuestionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    respostas = db.Column(db.Text) # Podemos armazenar as respostas como um JSON
    data_resposta = db.Column(db.DateTime(timezone=True), default=func.now())
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))

class Consulta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime(timezone=True))
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    psicologo_id = db.Column(db.Integer, db.ForeignKey('user.id'))