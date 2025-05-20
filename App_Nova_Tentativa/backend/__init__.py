# backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager() # Inicializa o LoginManager aqui
DB_NAME = 'site.db'
basedir = path.abspath(path.dirname(__file__))
instance_path = path.join(basedir, '..', 'instance')
database_path = path.join(instance_path, DB_NAME)

def create_app():
    app = Flask(__name__, instance_path=instance_path)
    app.config['SECRET_KEY'] = 'chave_secreta_para_seguranca'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    db.init_app(app)

    login_manager.init_app(app) # Associa o LoginManager à aplicação
    login_manager.login_view = 'routes.login'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User # Importa User aqui para evitar dependências circulares
        return User.query.get(int(user_id))

    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')

    from .models import User, Paciente, RegistroEmocao, RespostaQuestionario, Consulta

    with app.app_context():
        db.create_all()

    return app