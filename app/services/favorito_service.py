import logging
from typing import Union, List, Tuple, Dict, Any
from app import db
from app.models.Favorito import Favorito
from app.models.Atractivo import Atractivo
from app.models.Usuario import Usuario
from sqlalchemy import func

logger = logging.getLogger(__name__)

class FavoritoService:

    @staticmethod
    def validar_id(id_valor: Union[str, int]) -> Tuple[bool, Union[str, None]]:
        try:
            id_num = int(id_valor)
            if id_num <= 0:
                return False, "El ID debe ser un número positivo"
            return True, None
        except (ValueError, TypeError):
            return False, "El ID debe ser un número válido"

    @staticmethod
    def agregar_favorito(data: Dict[str, Any], usuario_id: int) -> Dict[str, Any]:
        if not data:
            return {'status': 'error', 'mensaje': 'No se recibieron datos', 'codigo': 400}

        if 'atractivo_id' not in data:
            return {'status': 'error', 'mensaje': 'Falta el campo obligatorio atractivo_id', 'codigo': 400}

        atractivo_id = data['atractivo_id']
        es_valido, error = FavoritoService.validar_id(atractivo_id)
        if not es_valido:
            return {'status': 'error', 'mensaje': error, 'codigo': 400}

        try:
            usuario = db.session.get(Usuario, usuario_id)
            if not usuario:
                return {'status': 'error', 'mensaje': 'Usuario no encontrado', 'codigo': 404}

            atractivo = db.session.get(Atractivo, int(atractivo_id))
            if not atractivo:
                return {'status': 'error', 'mensaje': f'Atractivo no encontrado con ID: {atractivo_id}', 'codigo': 404}

            favorito_existente = db.session.query(Favorito)\
                .filter_by(usuario_id=usuario_id, atractivo_id=int(atractivo_id))\
                .first()
            if favorito_existente:
                return {'status': 'existe', 'mensaje': 'Este atractivo ya está en favoritos'}

            nuevo_favorito = Favorito(usuario_id=usuario_id, atractivo_id=int(atractivo_id))
            db.session.add(nuevo_favorito)
            db.session.commit()

            return {'status': 'ok', 'favorito': nuevo_favorito}

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear favorito: {str(e)}")
            return {'status': 'error', 'mensaje': f'Error al crear favorito: {str(e)}', 'codigo': 500}

    @staticmethod
    def eliminar_favorito(favorito_id: int) -> Dict[str, Any]:
        es_valido, error = FavoritoService.validar_id(favorito_id)
        if not es_valido:
            return {'status': 'error', 'mensaje': error, 'codigo': 400}

        try:
            favorito = db.session.get(Favorito, favorito_id)
            if not favorito:
                return {'status': 'error', 'mensaje': 'Favorito no encontrado', 'codigo': 404}

            db.session.delete(favorito)
            db.session.commit()

            return {'status': 'ok'}

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar favorito: {str(e)}")
            return {'status': 'error', 'mensaje': f'Error al eliminar favorito: {str(e)}', 'codigo': 500}

    @staticmethod
    def obtener_favoritos_usuario_paginado(usuario_id: int, page: int = 1, per_page: int = 10) -> Tuple[List[Favorito], int]:
        offset = (page - 1) * per_page

        total = db.session.query(func.count(Favorito.id_favorito))\
            .filter(Favorito.usuario_id == usuario_id)\
            .scalar()

        favoritos = db.session.query(Favorito)\
            .filter(Favorito.usuario_id == usuario_id)\
            .order_by(Favorito.id_favorito.desc())\
            .offset(offset)\
            .limit(per_page)\
            .all()

        return favoritos, total

favorito_service = FavoritoService()
