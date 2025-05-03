from projet import mail
from flask_mail import Message
from flask import url_for


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Demande de réinitialisation du mot de passe de l'application Imasouk",
        sender="VOTRE EMAIL",
        recipients=[user.email],
        body=f"""Pour réinitialiser votre mot de passe, visitez le lien suivant:
        {url_for('users.reset_password', token=token, _external=True)}
        
        si vous n'êtes pas a l'origine de cette demande, veuillez ignorer cet e-mail.""",
    )
    mail.send(msg)
