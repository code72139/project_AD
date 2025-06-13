from app.models.Atractivo import Atractivo
from app.models.Favorito import Favorito

def obtener_atractivos_paginados(page: int, per_page: int, usuario_id: int) -> dict:
    consulta = (
        Atractivo.query
        .outerjoin(
            Favorito,
            (Favorito.atractivo_id == Atractivo.id_atractivo) &
            (Favorito.usuario_id == usuario_id)
        )
        .add_columns(Favorito.id_favorito)
        .order_by(Atractivo.id_atractivo)
    )

    paginacion = consulta.paginate(page=page, per_page=per_page, error_out=False)

    items = []
    for atractivo, id_favorito in paginacion.items:
        d = atractivo.to_dict()
        d['es_favorito'] = id_favorito is not None
        d['id_favorito'] = id_favorito
        items.append(d)

    return {
        'items': items,
        'metadata': {
            'page': page,
            'per_page': per_page,
            'total_items': paginacion.total,
            'total_pages': paginacion.pages,
            'has_next': paginacion.has_next,
            'has_prev': paginacion.has_prev
        }
    }
