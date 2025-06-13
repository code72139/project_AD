from app import db
from app.models.BaseModel import BaseModel

class Atractivo(BaseModel):
    __tablename__ = 'atractivos'

    id_atractivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    municipio = db.Column(db.String(100), nullable=False)
    tipo_de_atractivo = db.Column(db.String(100), nullable=False)
    subregion = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    comentarios = db.relationship('Comentario', back_populates='atractivo', lazy=True)
    favoritos = db.relationship('Favorito', back_populates='atractivo', lazy=True)

    __table_args__ = {'extend_existing': True}

    def __init__(self, municipio, tipo_de_atractivo, subregion, nombre, ubicacion, descripcion):
        self.municipio = municipio
        self.tipo_de_atractivo = tipo_de_atractivo
        self.subregion = subregion
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.descripcion = descripcion
