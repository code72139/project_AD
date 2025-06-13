import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Configuración de base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    
    # Configuración de la aplicación Flask
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1' # Cambiar a False en producción
    
    # URLs de APIs externas
    API_ATRACTIVOS_URL = os.getenv('API_ATRACTIVOS_URL')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    API_ATRACTIVOS_URL = "http://mock-api.test"
    API_TIMEOUT = 1