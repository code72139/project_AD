from app import db
from app.models.BaseModel import BaseModel

class Favorito(BaseModel):
    __tablename__ = 'favoritos'

    id_favorito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    atractivo_id = db.Column(db.Integer, db.ForeignKey('atractivos.id_atractivo'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='favoritos')
    atractivo = db.relationship('Atractivo', back_populates='favoritos', lazy=True)

    def __init__(self, usuario_id, atractivo_id):
        self.usuario_id = usuario_id
        self.atractivo_id = atractivo_id
