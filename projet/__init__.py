import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_modals import Modal
from flask_mail import Mail
from flask_admin import Admin

from projet.config import Config
from projet.adminbp.routes import MyModelView, MyAdminIndexView

# Initialisation des extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
modal = Modal()
mail = Mail()
admin = Admin(name='Imakayna', index_view=MyAdminIndexView(), template_mode='bootstrap3')

# Configuration de Flask-Login
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation des extensions avec app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    modal.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    # Importation des modèles et des blueprints après l'init de db
    from projet.models import User, Recette, Plat
    from projet.main.routes import main
    from projet.users.routes import users
    from projet.recettes.routes import recettes
    from projet.plats.routes import plats_bp
    from projet.errors.handlers import errors
    from projet.adminbp.routes import adminbp

    # Enregistrement des blueprints
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(recettes)
    app.register_blueprint(plats_bp)
    app.register_blueprint(errors)
    app.register_blueprint(adminbp, url_prefix="/admin")

    # Ajout des vues d'administration
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Recette, db.session))
    admin.add_view(MyModelView(Plat, db.session))

    return app
