from app import db
from app.models.BaseModel import BaseModel

class Usuario(BaseModel):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    favoritos = db.relationship('Favorito', back_populates='usuario')
    comentarios = db.relationship('Comentario', back_populates='usuario', lazy=True)

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password