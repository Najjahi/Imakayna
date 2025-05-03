from projet import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


with app.app_context():
    db.create_all()  # Crée les tables définies par les modèles
    print("Tables créées avec succès")