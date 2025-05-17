from flask import Blueprint, redirect, url_for, flash, render_template, abort
from projet import db
from projet.models import User, Recette, Plat
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from flask_admin import AdminIndexView
from functools import wraps


adminbp = Blueprint("adminbp", __name__)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('users.login'))  # Rediriger si l'utilisateur n'est pas admin

    def _template(self, **kwargs):
        # Tu peux ajouter des statistiques ou autres données spécifiques ici
        return render_template('admin/index.html', **kwargs)


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Recette, db.session))
admin.add_view(MyModelView(Plat, db.session))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # interdit
        return f(*args, **kwargs)
    return decorated_function

@adminbp.route('/myadmin')
@login_required
def myadmin_dashboard():
    return render_template('admin/myadmin.html')

# ========== UTILISATEURS ==========
@adminbp.route('/admin/utilisateurs')
@login_required
@admin_required
def liste_utilisateurs():
    users = User.query.all()
    return render_template("admin/utilisateurs.html", users=users)

# ========== RECETTES ==========
@adminbp.route('/admin/recettes')
@login_required
@admin_required
def liste_recettes():
    recettes = Recette.query.all()
    return render_template("admin/recettes.html", recettes=recettes)

# ========== PLATS ==========
@adminbp.route('/admin/plats')
@login_required
@admin_required
def liste_plats():
    plats = Plat.query.all()
    return render_template("admin/plats.html", plats=plats)