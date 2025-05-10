Flask App developed for Flask course on https://youtube.com/playlist?list=PL6X8IkNltYY_MgJNuEX- ◦ S1OABlAGOVUUw
 projet
python -m venv venv
venv\Scripts\activate
pip install flask
pip install flask-sqlalchemy
pip install Flask-Mail
pip install email-validator
pip install Flask-WTF 
pip install wtforms-sqlalchemy 
pip install Flask-Login 
pip install flask-modals
pip install flask-admin 
pip install Pillow
pip install flask-ckeditor
pip install Flask-Bcrypt
pip install Flask-Migrate
pip install python-dotenv
pip install bleach
pip install Flask==2.2.5

mkdir migrations\
flask db migrate -m "Ajout du champ is_approved"
flask db upgrade

flask db init
flask db migrate -m "Message de migration"

pip install --upgrade flask-admin flask flask-sqlalchemy wtforms wtforms-sqlalchemy flask-ckeditor Flask-Mail flask-modals Flask-Mail flask-admin Pillow Flask-WTF Flask-Login flask-mail email_validator Flask-Bcrypt Flask-Migrate Werkzeug==2.2.3 python-dotenvpy --upgrade Pillow --upgrade greenlet pip-tools Flask-Migrate Flask-Modals

from flask_admin.contrib.sqla import ModelView
pip install --upgrade flask-admin flask flask-sqlalchemy wtforms

pip install flask-ckeditor pour le m en forme du texte
pip install flask-modals pour javascript
 
pip install flask-admin Pillow
pip install Flask-WTF Flask-Login 
pip install Flask-Migrate
pip install flask==2.2.5pip 
install --upgrade flask_modals
pip install Werkzeug==2.2.3
pip install python-dotenv
pip install bleach
pip show jinja2
pip install --upgrade jinja2==3.0.3

Ctrl + Shift + P tape "Python: Select Interpreter" et sélectionne l'interpréteur dans ton venv
C:\Users\lenovo\Desktop\Pythonic-Flask\venv\Scripts\python.exe

pip install flask_wtf 
 pip install flask_bcrypt from flask_bcrypt import Bcrypt 
pip install flask_login
bcrypt  =Bcrypt() instance de la clase bcrypt
password = bcrypt.generate_password_hash('password').decode('utf-8')
 bcrypt.check_password_hash(hashed_password,'password123').decode('utf-8')
hashed_password = bcrypt.generate_password_hash('form.password.data').decode('utf-8')

def validate_username(self, username):username = User.query.filter_by(username.data).first()
 if user : raise ValidationError('username existe deja') methode wtform

from wtforms import Stringfield, PasswordField, submitField, BooleanField
from wtforms.validators import dataRequired, Length, Email, Regexp, Equalto, validationerror
from pythonic.models import User

ctr d pour modifier un plusiuers fois
lazy pour telecharger
formhidden_tag est 1 attribut de form instance pour proteger le formulaire
flash(f"compte cree for ^form.username.data",'succes') pour message

from flask import Flask, render_template, url_for,flask, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrqtionForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import db, LoginManager
from flask_login import UserMixin
from flask_login import login_user
login_manager = LoginManager(app) instance de la classe

login_user



@login_manager.user_loader   methode cherche user de la bd
def load_user(user_id):
	return User.query.get(int(user_id))

% with messages = get_flashed_messages(with_categories=true)% %if message% %for category, message%
div message /div %endfor% %endif% %endwith%



pyton import secrets 
secrets.token_hex(32) Click entree on copie on colle ds secret-KEY
pip install --upgrade flask


pip install -r requirements.txt
python.exe -m pip install --upgrade pip
.\.venv\Scripts\activate
$env:FLASK_APP = "run.py" 
venv) PS C:\Users\lenovo\Desktop\projetcnam>
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
flask run
>>

Usage: flask run [OPTIONS]
Try 'flask run --help' for help.

Error: Could not import 'app'.
(venv) PS C:\Users\lenovo\Desktop\projetcnam> 
from flask_bcrypt import Bcrypt
>>> Bcrypt()
bcrypt.generate_password_hash('password')

bcrypt.generate_password_hash('password').decode('utf-8')
<flask_bcrypt.Bcrypt object at 0x000001CDC4924C20>                  ode('utf-8')
>>> bcrypt = Bcrypt()
>>> hashed_password = bcrypt.generate_password_hash('password').deccode('utf-8')
>>> bcrypt.check_password_hash(hashed_password, 'password')
hashed_password = bcrypt.generate_password_hash('form.password.data').decode('utf-8')
omar@gmail.com
PASS!!word123
password R@yane2017

from projet import db
from projet.models import User

from projet import User, recette, Cuisine

user_1 = User(fname = 'imane', lname = 'najjahi', username = 'imane' email = 'imane@gmail.com', password = 'R@yane1917')
db.session.add(user_1)

user_2 = User(fname='anas', lname='najjahi', username='anas', email='anas@gmail.com', password='R@yane1917')

db.session.add(user_2)
db.session.add(user_1)
db.session.commit()

db.drop_all()
db.create_all()
User.query.all()




from itsdangerous import URLSafeTimedSerializer
>>>
>>> s = URLSafeTimedSerializer('supersecret')
>>> token = s.dumps({'user_id':1}) #1 c a d 1 heure
>>> token
'eyJ1c2VyX2lkIjoxfQ.Z8iXUA.XWJebQM4qMc7xcAee_wMYLMhbTg'
Imasouk2025  Imasoukcnam
Le01011954 imasoukcnam@gmail.com
ztop dgeg hjxg ywip
de51a48395fd0c521776b6b54fd8a0e7
P@ssw0rd

>>>> from projet import app
>>> from projet.models import db, Plat, User
>>> with app.app_context():
...     plats = Plat.query.all()
...     print("Plats :", plats)


Plats : [Plat('tagine aux pruneaux'), Plat('Seffa au poulet'), Plat('couscous'), Plat('Nos desserts'), Plat('Nos entrées'), Plat('Plat principal')]>>> 

>>> from projet.models import db, Recette, Plat
>>> with app.app_context():
...     plats = Plat.query.all()
...     for plat in plats:
...             db.session.delete(plat)
...     db.session.commit()
...     print("Tous les plats ont été supprimés.")

>>> from projet.models import db, Recette, Plat
>>> with app.app_context():
...     recettes = Recette.query.all()
...     for recette in recettes:
...             db.session.delete(recette)
...     db.session.commit()
...     print("Toutes les recettes ont été supprimés.")




https://dbdiagram.io/d/67ed0dd84f7afba18411e146  mpd par yamina 
https://demo.bpmn.io/new  bpmn par yamina
https://www.jdoodle.com/online-java-compiler

mysql Root Root Imane p@ssw0rd

Remove-Item -Recurse -Force venv

>>> from projet import app
>>> from projet import db
>>> from projet.models import User
>>> 
>>> with app.app_context():
...     user = User.query.first()
...     print(user)
...
User('imane', 'NAJJAHI', 'imane najjahi', 'najjahiimane@gmail.com', 'default.png')
>>> with app.app_context():
...     users = User.query.all()
...     for user in users:
...         print(user)
...
KeyboardInterrupt
>>> from projet import app, db
>>> from projet.models import User
>>>
>>> with app.app_context():
...     users = User.query.all()
...     for user in users:
...         print(user)
...
KeyboardInterrupt
>>> for user in users:
...     print(user.prenom, user.nom, user.email)
...
KeyboardInterrupt
>>> with app.app_context():
...     count = User.query.count()
...     print(f"Nombre d'utilisateurs : {count}")
...
Nombre d'utilisateurs : 3
>>> with app.app_context():
...     users = User.query.all()
...     for user in users:
...         print(user)
... 
User('imane', 'NAJJAHI', 'imane najjahi', 'najjahiimane@gmail.com', 'default.png')
User('imane', 'NAJJAHI', 'imane', 'imane@gmail.com', '2a507317bf145bc8.png')
User('lina', 'marhri', 'lina', 'lina@gmail.com', 'a18e787698408e11.png')

>>> with app.app_context():
...     user = User.query.filter_by(username='imane').first()
...     print(user.recettes)
...
[Recette('Seffa au poulet', '2025-04-27 11:01:50.224078'), Recette('pastilla poulet amandes', '2025-04-27 11:16:10.195609')]

flag est une variable booléenne (vrai ou faux)
Serializer est une classe fournie par la bibliothèque itsdangerous Elle permet de Signer des données pour les sécuriser: Sérialise des données Python en chaîne de caractères sécurisée  (comme un token dans un lien). Puis peut désérialiser (décoder) cette chaîne plus tard.
path est le chemin relatif vers le dossier où je veux enregistrer l'image ("static/user_pics").
os Fait partie de la bibliothèque standard Python, il Sert à manipuler les chemins de fichiers, de manière sûre entre OS.
CKEDITOR_ENABLE_CODESNIPPET active le plugin “CodeSnippet” dans CKEditor, Ce plugin permet d’insérer des blocs de code bien formatés et colorés 
RequestResetForm : Demande Réinitialiser Formulaire
Blueprint est une manière de modulariser une application Flask. Il permet de regrouper des routes, des templates, des formulaires, etc., dans un module logique indépendant.
abort est une fonction dans Flask qui permet d'arrêter l'exécution d'une vue et renvoyer un code de statut HTTP spécifique. Cela permet de renvoyer des erreurs HTTP personnalisées.
