from app import db
from app.models.Comentario import Comentario
from app.models.Atractivo import Atractivo
from app.models.Usuario import Usuario
import logging

logger = logging.getLogger(__name__)

class ComentarioError(Exception):
    pass

class ComentarioService:
    @staticmethod
    def obtener_comentarios():
        try:
            comentarios = Comentario.query.all()
            logger.info(f"Obtenidos {len(comentarios)} comentarios")
            return comentarios
        except Exception as e:
            mensaje = f"Error al obtener todos los comentarios: {str(e)}"
            logger.error(mensaje)
            raise ComentarioError(mensaje)

    @staticmethod
    def obtener_comentarios_por_atractivo(atractivo_id, page=1, per_page=10):
        try:
            atractivo = db.session.get(Atractivo, atractivo_id)
            if not atractivo:
                mensaje = f"Atractivo no encontrado con ID: {atractivo_id}"
                logger.warning(mensaje)
                return {"items": [], "metadata": {"total": 0, "page": page, "per_page": per_page, "total_pages": 0}}
            
            pagination = Comentario.query.filter_by(atractivo_id=atractivo_id)\
                .order_by(Comentario.fecha_creacion.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            response = {
                "items": [c.to_dict() for c in pagination.items],
                "metadata": {
                    "total": pagination.total,
                    "page": page,
                    "per_page": per_page,
                    "total_pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev
                }
            }
            
            logger.info(f"Obtenidos {len(pagination.items)} comentarios para el atractivo {atractivo_id} (página {page})")
            return response
        except Exception as e:
            mensaje = f"Error al obtener comentarios del atractivo {atractivo_id}: {str(e)}"
            logger.error(mensaje)
            raise ComentarioError(mensaje)

    @staticmethod
    def crear_comentario(atractivo_id, texto, usuario_id=1):
        try:
            if not atractivo_id or not isinstance(atractivo_id, int) or atractivo_id <= 0:
                raise ComentarioError("ID de atractivo inválido.")
            if not usuario_id or not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ComentarioError("ID de usuario inválido.")
            if not texto or texto.strip() == "":
                raise ComentarioError("El texto del comentario no puede estar vacío.")
            
            logger.info(f"Intentando crear comentario - atractivo_id: {atractivo_id}, usuario_id: {usuario_id}")
            
            usuario = db.session.get(Usuario, usuario_id)
            if not usuario:
                raise ComentarioError(f"Usuario no encontrado: {usuario_id}")
            
            atractivo = db.session.get(Atractivo, atractivo_id)
            if not atractivo:
                raise ComentarioError(f"Atractivo no encontrado: {atractivo_id}")
            
            nuevo_comentario = Comentario(
                texto=texto.strip(),
                usuario_id=usuario_id,
                atractivo_id=atractivo_id
            )
            db.session.add(nuevo_comentario)
            db.session.commit()
            
            logger.info(f"Comentario creado: usuario {usuario_id}, atractivo {atractivo_id}")
            return nuevo_comentario.to_dict()
            
        except ComentarioError as ce:
            logger.warning(str(ce))
            raise
        except Exception as e:
            db.session.rollback()
            mensaje = f"Error al crear comentario: {str(e)}"
            logger.error(mensaje)
            raise ComentarioError(mensaje)

    @staticmethod
    def eliminar_comentario(comentario_id):
        try:
            comentario = db.session.get(Comentario, comentario_id)
            if not comentario:
                raise ComentarioError(f"Comentario no encontrado: {comentario_id}")
            
            db.session.delete(comentario)
            db.session.commit()
            
            logger.info(f"Comentario eliminado: {comentario_id}")
            return True
        except ComentarioError:
            raise
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar comentario: {str(e)}")
            raise ComentarioError(f"Error al eliminar comentario: {str(e)}")

    @staticmethod
    def editar_comentario(comentario_id, nuevo_texto):
        try:
            if not nuevo_texto or nuevo_texto.strip() == "":
                raise ComentarioError("El texto del comentario no puede estar vacío.")
            
            comentario = db.session.get(Comentario, comentario_id)
            if not comentario:
                raise ComentarioError(f"Comentario no encontrado: {comentario_id}")

            comentario.texto = nuevo_texto.strip()
            db.session.commit()
            
            logger.info(f"Comentario editado: {comentario_id}")
            return comentario.to_dict()
        except ComentarioError:
            raise
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al editar comentario: {str(e)}")
            raise ComentarioError(f"Error al editar comentario: {str(e)}")

comentario_service = ComentarioService()
