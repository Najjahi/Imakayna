from flask import Blueprint, current_app
import os
import secrets
from projet.models import User, Recette
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
)
from projet.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateProfileForm,
    RequestResetForm,
    ResetPasswordForm,
    ProfileForm,
)
from projet import bcrypt, db
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)
from projet.helpers import save_picture
from projet.users.forms import DeletePictureForm
from projet.users.helpers import send_reset_email
from PIL import Image  # Assurez-vous que Pillow est installé

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Compte créé avec succès pour {form.username.data}", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Vous avez été connecté!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Connexion infructueuse. Veuillez vérifier les informations d’identification", "danger")
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", active_tab=None)


# Fonction pour sauvegarder l'image de profil
def save_picture(form_picture, folder_name, output_size=(125, 125)):
    # Vérifie que le dossier existe
    os.makedirs(folder_name, exist_ok=True)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(folder_name, picture_fn)

    # Créer le dossier s'il n'existe pas
    os.makedirs(folder_name, exist_ok=True)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# Fonction combinée pour afficher et mettre à jour le profil
@users.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = UpdateProfileForm()

    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            print("📂 Un fichier a été reçu :", profile_form.picture.data.filename)

            picture_file = save_picture(
                profile_form.picture.data,
                os.path.join(current_app.root_path, "static/user_pics"),
                output_size=(150, 150)
            )
            current_user.image_file = picture_file
        else:
            print("⚠️ Aucun fichier image reçu")

        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()

        flash("Votre profil a été mis à jour", "success")
        return redirect(url_for("users.profile"))

    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio

    image_file = url_for("static", filename=f"user_pics/{current_user.image_file or 'default.jpg'}")

    return render_template(
        "profile.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",
    )

@users.route("/delete_profile_picture", methods=['POST'])
@login_required
def delete_profile_picture():
    if current_user.image_file != 'default.jpg':
        image_path = os.path.join(current_app.root_path, 'static/user_pics', current_user.image_file)
        # Vérifie si le fichier existe avant de le supprimer
        if os.path.exists(image_path):
            os.remove(image_path)
        current_user.image_file = 'default.jpg'
        db.session.commit()
        flash('Photo de profil supprimée.', 'info')
    else:
        flash('Aucune photo personnalisée à supprimer.', 'warning')

    return redirect(url_for('users.profile'))  # ou l’endroit où tu reviens

@users.route("/author/<string:username>", methods=["GET"])
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    recettes = (
        Recette.query.filter_by(author=user)
        .order_by(Recette.date_posted.desc())
        .paginate(page=page, per_page=6)
    )
    return render_template("author.html", recettes=recettes, user=user)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash(
            "Si ce compte existe, vous recevrez un e-mail avec des instructions", "info",
        )
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Le jeton n’est pas valide ou a expiré", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Votre mot de passe a été mis à jour. Vous pouvez maintenant vous connecter", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Reset Password", form=form)

def profile():
    form = UpdateProfileForm()
    delete_form = DeletePictureForm()

