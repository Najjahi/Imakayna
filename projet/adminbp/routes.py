from flask import Blueprint, redirect, url_for, flash, render_template
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user, login_required
from functools import wraps

adminbp = Blueprint("adminbp", __name__)

# ===== VUES ADMIN =====
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "is_admin", False)

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('users.login'))


# ===== VUES DE L'ADMIN =====
@adminbp.route('/myadmin')
@login_required
def myadmin_dashboard():
    return render_template('admin/myadmin.html')


# ========== UTILISATEURS ==========
@adminbp.route('/admin/utilisateurs')
@login_required
def liste_utilisateurs():
    from projet.models import User
    users = User.query.all()
    return render_template("admin/utilisateurs.html", users=users)

# ========== RECETTES ==========
@adminbp.route('/admin/recettes')
@login_required
def liste_recettes():
    from projet.models import Recette
    recettes = Recette.query.all()
    return render_template("admin/recettes.html", recettes=recettes)

# ========== PLATS ==========
@adminbp.route('/admin/plats')
@login_required
def liste_plats():
    from projet.models import Plat
    plats = Plat.query.all()
    return render_template("admin/plats.html", plats=plats)

# ========== APPROUVER RECETTES ==========
@adminbp.route('/admin/recettes_en_attente')
@login_required
def recettes_en_attente():
    from projet.models import Recette
    recettes = Recette.query.filter_by(status='en_attente').all()  # selon ton modèle
    return render_template('admin/recettes_en_attente.html', recettes=recettes)
