from app import create_app, db

app = create_app()

def crear_tablas():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    crear_tablas()
    app.run(host="0.0.0.0", port=5000)
