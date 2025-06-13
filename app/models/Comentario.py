from app import db
from datetime import datetime
from app.models.BaseModel import BaseModel


class Comentario(BaseModel):
    __tablename__ = 'comentarios'

    id_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    atractivo_id = db.Column(db.Integer, db.ForeignKey('atractivos.id_atractivo'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='comentarios', lazy=True)
    atractivo = db.relationship('Atractivo', back_populates='comentarios', lazy=True)

    def __init__(self, texto, usuario_id, atractivo_id):
        self.texto = texto
        self.usuario_id = usuario_id
        self.atractivo_id = atractivo_id

    def to_dict(self):
        """Convierte el comentario a un diccionario"""
        return {
            'id': self.id_comentario,
            'texto': self.texto,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_id': self.usuario_id,
            'atractivo_id': self.atractivo_id
        }
