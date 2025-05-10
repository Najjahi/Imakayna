from flask import Blueprint, request, redirect, url_for, flash
from projet import db
from projet.models import Recette, Plat
from flask import (
    render_template,
)
from flask_login import current_user
   
plats_bp = Blueprint("plats", __name__)

@plats_bp.route("/<string:plat_title>")
def plat(plat_title):
    plat = Plat.query.filter_by(title=plat_title).first()
    plat_id = plat.id if plat else None
    plat = Plat.query.get_or_404(plat_id)
    page = request.args.get("page", 1, type=int)
    recettes = Recette.query.filter_by(plat_id=plat_id).paginate(
        page=page, per_page=6
    )
    return render_template(
        "plat.html",
        title=plat.title,
        plat=plat,
        recettes=recettes,
    )

@plats_bp.route("/plats")
def plats():
    page = request.args.get("page", 1, type=int)
    plats = Plat.query.paginate(page=page, per_page=6)
    return render_template("plats.html", title="plats", plats=plats)

# Suppression d'un plat

@plats_bp.route("/plat/<int:plat_id>/delete", methods=["POST"])
def delete_plat(plat_id):
    plat = Plat.query.get_or_404(plat_id)
    
    # Vérifier si l'utilisateur est l'auteur du plat ou un administrateur
    if plat.author != current_user and not current_user.is_admin:
        flash("Vous n'êtes pas autorisé à supprimer ce plat.", "danger")
        return redirect(url_for("plats.plats"))
    
    db.session.delete(plat)
    db.session.commit()
    
    flash("Le plat a bien été supprimé.", "success")
    return redirect(url_for("plats.plats"))