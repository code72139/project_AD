from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app(testing=False):
    app = Flask(__name__)

    # Configuración base
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        app.config.from_object(Config)

    db.init_app(app)

    # Importar y registrar blueprints
    from app.controllers.favorito_controller import favorito_bp
    from app.controllers.comentario_controller import comentario_bp
    from app.controllers.atractivo_controller import atractivo_bp

    app.register_blueprint(favorito_bp)
    app.register_blueprint(comentario_bp)
    app.register_blueprint(atractivo_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app