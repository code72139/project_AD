from flask import jsonify, session
from app.models.Usuario import Usuario
from app import db

def seleccionar_usuario(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    session['usuario_id'] = usuario_id
    return jsonify({'mensaje': f'Usuario {usuario.nombre} seleccionado'})
