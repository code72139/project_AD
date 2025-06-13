from flask import Blueprint, jsonify, request
from app.services import obtener_atractivos_paginados

atractivo_bp = Blueprint('atractivo', __name__)

@atractivo_bp.route('/atractivos', methods=['GET'])
def listar_atractivos():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        usuario_id = 1

        response = obtener_atractivos_paginados(page, per_page, usuario_id)
        return jsonify(response)

    except Exception as e:
        print(f"Error al obtener atractivos: {str(e)}")
        return jsonify({'error': f'Error al obtener atractivos: {str(e)}'}), 500
