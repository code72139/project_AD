from flask import Blueprint, jsonify, request
from app.services import comentario_service

comentario_bp = Blueprint('comentario', __name__)

@comentario_bp.route('/comentarios', methods=['GET'])
def listar_comentarios():
    try:
        comentarios = comentario_service.obtener_comentarios()
        return jsonify([c.to_dict() for c in comentarios]), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener los comentarios', 'detalle': str(e)}), 500

@comentario_bp.route('/comentarios/atractivo/<int:atractivo_id>', methods=['GET'])
def listar_comentarios_por_atractivo(atractivo_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        resultado = comentario_service.obtener_comentarios_por_atractivo(atractivo_id, page, per_page)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener los comentarios', 'detalle': str(e)}), 500

@comentario_bp.route('/comentarios', methods=['POST'])
def agregar_comentario():
    try:
        data = request.get_json() or {}

        comentario = comentario_service.crear_comentario(
            atractivo_id=data.get('atractivo_id'),
            texto=data.get('texto'),
            usuario_id=1
        )

        if isinstance(comentario, str):
            return jsonify({'error': comentario}), 400

        return jsonify(comentario), 201

    except Exception as e:
        return jsonify({'error': 'Error al agregar el comentario', 'detalle': str(e)}), 500

@comentario_bp.route('/comentarios/<int:comentario_id>', methods=['DELETE'])
def eliminar_comentario(comentario_id):
    try:
        resultado = comentario_service.eliminar_comentario(comentario_id)

        if isinstance(resultado, str):
            return jsonify({'error': resultado}), 404

        return jsonify({'mensaje': 'Comentario eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error al eliminar el comentario', 'detalle': str(e)}), 500

@comentario_bp.route('/comentarios/<int:comentario_id>', methods=['PUT'])
def editar_comentario(comentario_id):
    try:
        data = request.get_json() or {}

        resultado = comentario_service.editar_comentario(comentario_id, data.get('texto'))

        if isinstance(resultado, str):
            return jsonify({'error': resultado}), 404

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({'error': 'Error al editar el comentario', 'detalle': str(e)}), 500
