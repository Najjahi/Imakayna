from datetime import datetime
from projet import db, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    recettes = db.relationship("Recette", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)


    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"], salt="pw-reset")
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(current_app.config["SECRET_KEY"], salt="pw-reset")
        try:
            user_id = s.loads(token, max_age=age)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"

class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(20), nullable=False, default="default_thumbnail.jpg" )
    slug = db.Column(db.String(32), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    plat_id = db.Column(db.Integer, db.ForeignKey("plat.id"), nullable=False)

    def __repr__(self): #méthode python permet de rendre l’objet plus compréhensible quand il est affiché.
        return f"Recette('{self.title}', '{self.date_posted}')"

class Plat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(20), nullable=False, default="default_icon.jpg")
    recettes = db.relationship("Recette", backref="plat_name", lazy=True)
        
    def __repr__(self):
        return f"Plat('{self.title}')"
    def save_slug(self):
        """Méthode pour générer le slug à partir du titre"""
        self.slug = self.title.lower().replace(" ", "-")
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recette_id = db.Column(db.Integer, db.ForeignKey("recette.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
       
    def __repr__(self):
        return f"Comment('{self.content[:20]}...','{self.date_posted}')"
