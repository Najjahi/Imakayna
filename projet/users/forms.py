from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from projet.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
)
#'a56119fc45284ec5b42d3c0fecf067646bb33ec274a836e4b191bc5eac346b47'
class RegistrationForm(FlaskForm):
    fname = StringField(
        "Prénom", validators=[DataRequired(), Length(min=2, max=25)]
    )
    lname = StringField("Nom", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(
        "Nom d'utilisateur", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe",
        validators=[
            DataRequired(),
            Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),
        ],
    )
    confirm_password = PasswordField(
        "Confirmation du mot de passe", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Ce nom d'utilisateur existe déjà ! Veuillez en choisir un autre"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Cet Email existe déjà ! Veuillez en choisir un autre")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")


class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Nom d'utilisateur", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio")
    picture = FileField(
        "Mettre à jour la photo de profil", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Modifier")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Ce Nom d'utilisateur existe déjà ! Veuillez en choisir un autre"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "Cet Email existe déjà ! Veuillez en choisir un autre"
                )

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Initialiser Votre Mot de passe')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
             Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$"),
    ],
    )
    confirm_password = PasswordField(
        "Confirmation du mot de passe", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Initialiser Mot de passe")