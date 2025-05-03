from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from projet.models import Plat
from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length

def choice_query():
    return Plat.query

class NewRecetteForm(FlaskForm):
    plat = QuerySelectField("Plat", query_factory=choice_query, get_label="title")
    title = StringField("Titre de la Recette", validators=[DataRequired(), Length(max=100)])
    slug = StringField(
        "Slug",
        validators=[DataRequired(), Length(max=32)],
        render_kw={
            "placeholder": "Version courte et descriptive de notre titre. Optimisé pour le référencement"
        },
    )
    content = CKEditorField(
        "Contenu de la Recette", validators=[DataRequired()], render_kw={"rows": "20"}
    )
    thumbnail = FileField(
        "Thumbnail", validators=[DataRequired(), FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Post")


class RecetteUpdateForm(NewRecetteForm):
    thumbnail = FileField("Thumbnail", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")
