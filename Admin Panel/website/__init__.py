from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "deproject.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'nceancjkcadsvnak'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:\\Users\\NITIN\\Documents\\LDCE\\SEM-6\\DE\\Smart-career-guider\\instance\\{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Admin, Expert

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
