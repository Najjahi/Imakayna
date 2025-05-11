from dotenv import load_dotenv
import os
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

load_dotenv() # Charger les variables d'environnement

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///cuisine.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #désactive une fonctionnalité coûteuse inutile si non utilisée
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = "main.upload"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    FLASK_ENV = os.environ.get("FLASK_ENV")  # Ajouté dans la classe de config
    DEBUG = FLASK_ENV == 'development'  # Active le debug si l'environnement est 'development'

