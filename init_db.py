from app import create_app, db

def init_database():
    app = create_app()
    with app.app_context():
        print("Creando tablas en la base de datos...")
        db.create_all()
        print("¡Base de datos inicializada correctamente!")

if __name__ == '__main__':
    init_database()
