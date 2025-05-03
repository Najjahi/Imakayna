from flask import Blueprint
from projet.models import Recette, Plat
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    session,
    abort,
)
from projet.recettes.forms import (
    NewRecetteForm,
    RecetteUpdateForm,
)
from projet.plats.forms import NewPlatForm

from projet import db
from flask_modals import render_template_modal
from flask_login import (
    login_required,
    current_user,
)
from projet.helpers import save_picture
from projet.recettes.helpers import get_precedente_suivante_recette, delete_picture
from flask import g

recettes = Blueprint("recettes", __name__)


@recettes.route("/dashboard/new_recette", methods=["GET", "POST"])
@login_required
def new_recette():
    new_recette_form = NewRecetteForm()
    new_plat_form = NewPlatForm()
    form = ""
    flag = session.pop("flag", False)
    if "content" in request.form:
        form = "new_recette_form"
    elif "description" in request.form:
        form = "new_plat_form"

    if form == "new_recette_form" and new_recette_form.validate_on_submit():
        if new_recette_form.thumbnail.data:
            picture_file = save_picture(
                new_recette_form.thumbnail.data, "static/recette_thumbnails"
            )
        recette_slug = str(new_recette_form.slug.data).replace(" ", "-")
        plat = new_recette_form.plat.data
        recette = Recette(
            title=new_recette_form.title.data,
            content=new_recette_form.content.data,
            slug=recette_slug,
            author=current_user,
            plat_name=plat,
            thumbnail=picture_file,
        )
        db.session.add(recette)
        db.session.commit()
        flash("Votre recette a bien été créee!", "success")
        return redirect(url_for("recettes.new_recette"))

    elif form == "new_plat_form" and new_plat_form.validate_on_submit():
        if new_plat_form.icon.data:
            picture_file = save_picture(
                new_plat_form.icon.data, "static/plat_icons", output_size=(150, 150)
            )
        plat_title = str(new_plat_form.title.data).replace(" ", "-")
        plat = Plat(
            title=new_plat_form.title.data,
            description=new_plat_form.description.data,
            icon=picture_file,
        )
        db.session.add(plat)
        db.session.commit()
        session["flag"] = True
        flash("Ce nouveau plat a bien été crée!", "success")
        return redirect(url_for("users.dashboard"))

    modal = None if flag else "newPlat"
    return render_template_modal(
    
    
        "new_recette.html",
        title="New Recette",
        new_recette_form=new_recette_form,
        new_plat_form=new_plat_form,
        active_tab="new_recette",
        modal=modal,
    )


@recettes.route("/<string:plat>/<string:recette_slug>")
def recette(recette_slug, plat):
    recette = Recette.query.filter_by(slug=recette_slug).first()
    if recette:
        precedente_recette, suivante_recette = get_precedente_suivante_recette(recette)
    recette_id = recette.id if recette else None
    recette = Recette.query.get_or_404(recette_id)
    return render_template(
        "recette_view.html",
        title=recette.title,
        recette=recette,
        precedente_recette=precedente_recette,
        suivante_recette=suivante_recette,
    )


@recettes.route("/dashboard/user_recettes", methods=["GET", "POST"])
@login_required
def user_recettes():
    print("current_user =", current_user)
    print("Recettes =", current_user.recettes)
    print("Active tab = user_recettes")
    recettes_user = current_user.recettes
    return render_template(
        "user_recettes.html",  # PAS "dashboard.html" ici !
        title="Vos Recettes",
        active_tab="user_recettes",
        recettes=recettes_user,
    )


@recettes.route("/<string:plat>/<string:recette_slug>/update", methods=["GET", "POST"])
def update_recette(recette_slug, plat):
    recette = Recette.query.filter_by(slug=recette_slug).first()
    if recette:
        precedente_recette, suivante_recette = get_precedente_suivante_recette(recette)
    recette_id = recette.id if recette else None
    recette = Recette.query.get_or_404(recette_id)
    if recette.author != current_user:
        abort(403)
    form = RecetteUpdateForm()
    if form.validate_on_submit():
        recette.plat_name = form.plat.data
        recette.title = form.title.data
        recette.slug = str(form.slug.data).replace(" ", "-")
        recette.content = form.content.data
        if form.thumbnail.data:
            delete_picture(recette.thumbnail, "static/recette_thumbnails")
            new_picture = save_picture(form.thumbnail.data, "static/recette_thumbnails")
            recette.thumbnail = new_picture
        db.session.commit()
        flash("Votre recette a bien été modifiée!", "success")
        return redirect(
            url_for("recettes.recette", recette_slug=recette.slug, plat=recette.plat_name.title)
        )
    elif request.method == "GET":
        form.plat.data = recette.plat_name.title
        form.title.data = recette.title
        form.slug.data = recette.slug
        form.content.data = recette.content
    return render_template(
        "update_recette.html",
        title="Update | " + recette.title,
        recette=recette,
        precedente_recette=precedente_recette,
        suivante_recette=suivante_recette,
        form=form,
    )


@recettes.route("/recette/<recette_id>/delete", methods=["POST"])
def delete_recette(recette_id):
    recette = Recette.query.get_or_404(recette_id)
    if recette.author != current_user:
        abort(403)
    db.session.delete(recette)
    db.session.commit()
    flash("Votre recette a bien été supprimé!", "success")
    return redirect(url_for("recettes.user_recettes"))
