from flask import Blueprint, redirect, url_for, flash, render_template, abort
from projet import admin, db
from projet.models import User, Recette, Plat
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import AdminIndexView
from functools import wraps

adminbp = Blueprint("adminbp", __name__)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return False

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



@adminbp.route('/admin/recettes_en_attente')
@admin_required  # un décorateur qui vérifie que l'utilisateur est admin
def recettes_en_attente():
    recettes = Recette.query.filter_by(is_approved=False).all()
    return render_template('admin/recettes_en_attente.html', recettes=recettes)

@adminbp.route('/admin/approve_recette/<int:recette_id>')
@admin_required
def approve_recette(recette_id):
    recette = Recette.query.get_or_404(recette_id)
    recette.is_approved = True
    db.session.commit()
    flash("Recette approuvée avec succès.", "success")
    return redirect(url_for('recettes_en_attente'))

