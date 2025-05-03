from flask import Blueprint, request

from projet.models import Recette, Plat
from flask import (
    render_template,
)

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
