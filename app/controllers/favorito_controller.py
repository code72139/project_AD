from flask import Blueprint, jsonify, request, render_template
from typing import Tuple, Dict, Any
from app.services import favorito_service
from app.models.Favorito import Favorito

favorito_bp = Blueprint('favorito', __name__)

def _serializar_favorito(favorito: Favorito) -> Dict[str, Any]:
    return {
        'id': favorito.id_favorito,
        'usuario_id': favorito.usuario_id,
        'atractivo_id': favorito.atractivo_id,
        'atractivo': {
            'id': favorito.atractivo.id_atractivo,
            'nombre': favorito.atractivo.nombre,
            'descripcion': favorito.atractivo.descripcion
        } if favorito.atractivo else None
    }

@favorito_bp.route('/api/favoritos', methods=['POST'])
def agregar_favorito() -> Tuple[Dict[str, Any], int]:
    try:
        data = request.get_json()
        usuario_id = 1

        resultado = favorito_service.agregar_favorito(data, usuario_id)
        
        if resultado['status'] == 'error':
            return jsonify({'error': resultado['mensaje']}), resultado.get('codigo', 400)
        elif resultado['status'] == 'existe':
            return jsonify({'mensaje': resultado['mensaje']}), 200
        
        favorito_serializado = _serializar_favorito(resultado['favorito'])
        return jsonify({'mensaje': 'Favorito agregado correctamente', 'favorito': favorito_serializado}), 201

    except Exception as e:
        return jsonify({'error': 'Error al crear el favorito', 'detalle': str(e)}), 500

@favorito_bp.route('/api/favoritos/<int:favorito_id>', methods=['DELETE'])
def eliminar_favorito(favorito_id: int) -> Tuple[Dict[str, Any], int]:
    try:
        resultado = favorito_service.eliminar_favorito(favorito_id)

        if resultado['status'] == 'error':
            return jsonify({'error': resultado['mensaje']}), resultado.get('codigo', 404)
        
        return jsonify({'mensaje': 'Favorito eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error al eliminar el favorito', 'detalle': str(e)}), 500

@favorito_bp.route('/favoritos', methods=['GET'])
def vista_favoritos():
    return render_template('favoritos.html')

@favorito_bp.route('/api/favoritos', methods=['GET'])
def obtener_favoritos():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        usuario_id = 1

        favoritos, total = favorito_service.obtener_favoritos_usuario_paginado(usuario_id, page, per_page)
        favoritos_serializados = [_serializar_favorito(fav) for fav in favoritos]

        return jsonify({
            'favoritos': favoritos_serializados,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page
        }), 200

    except Exception as e:
        return jsonify({'error': 'Error al obtener favoritos', 'detalle': str(e)}), 500
