from app.services import favorito_service
from app.models.Usuario import Usuario
from app.models.Atractivo import Atractivo
from app.models.Favorito import Favorito

def test_agregar_favorito(db_session):
    engine = db_session.get_bind()
    print(f"Usando BD: {engine.url}")
    usuario = Usuario(nombre="Jose", email="jose@test.com", password="1234")
    atractivo = Atractivo(
        municipio="Test Town",
        tipo_de_atractivo="Cultural",
        subregion="Sur",
        nombre="Museo X",
        ubicacion="Calle 45",
        descripcion="Un museo interesante"
    )

    db_session.add_all([usuario, atractivo])
    db_session.commit()

    data = {"atractivo_id": atractivo.id_atractivo}
    resultado = favorito_service.agregar_favorito(data, usuario.id_usuario)

    assert resultado["status"] == "ok"
    favorito = resultado["favorito"]
    assert favorito.usuario_id == usuario.id_usuario
    assert favorito.atractivo_id == atractivo.id_atractivo

def test_agregar_favorito_usuario_no_existe(db_session):
    atractivo = Atractivo(municipio="Test Town", tipo_de_atractivo="Cultural", subregion="Sur",
                          nombre="Museo X", ubicacion="Calle 45", descripcion="Un museo interesante")
    db_session.add(atractivo)
    db_session.commit()

    data = {"atractivo_id": atractivo.id_atractivo}
    resultado = favorito_service.agregar_favorito(data, usuario_id=9999)

    assert resultado["status"] == "error"
    assert "Usuario no encontrado" in resultado["mensaje"]


def test_eliminar_favorito_existe(db_session):
    usuario = Usuario(nombre="Ana", email="ana@test.com", password="1234")
    atractivo = Atractivo(
        municipio="Ciudad X",
        tipo_de_atractivo="Natural",
        subregion="Norte",
        nombre="Parque Y",
        ubicacion="Avenida 123",
        descripcion="Un parque natural"
    )
    db_session.add_all([usuario, atractivo])
    db_session.commit()

    favorito = Favorito(usuario_id=usuario.id_usuario, atractivo_id=atractivo.id_atractivo)
    db_session.add(favorito)
    db_session.commit()

    resultado = favorito_service.eliminar_favorito(favorito.id_favorito)

    assert resultado["status"] == "ok"

    favorito_buscado = db_session.get(Favorito, favorito.id_favorito)
    assert favorito_buscado is None

def test_eliminar_favorito_no_existe(db_session):
    resultado = favorito_service.eliminar_favorito(9999)  

    assert resultado["status"] == "error"
    assert "Favorito no encontrado" in resultado["mensaje"]

def test_eliminar_favorito_id_invalido(db_session):
    resultado = favorito_service.eliminar_favorito(-5)

    assert resultado["status"] == "error"
    assert "El ID debe ser un número positivo" in resultado["mensaje"]