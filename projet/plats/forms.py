from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from projet.models import Plat
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
)


class NewPlatForm(FlaskForm):
    title = StringField("Le nom du Plat", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(
        "Description du Plat", validators=[DataRequired(), Length(max=150)]
    )
    icon = FileField("Icon", validators=[DataRequired(), FileAllowed(["jpg", "png"])])
    submit = SubmitField("Create")

    def validate_title(self, title):
        course = Plat.query.filter_by(title=title.data).first()
        if course:
            raise ValidationError(
                "Ce nom de plateforme existe déjà ! Veuillez en choisir un autre."
            )
