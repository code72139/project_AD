import requests
from requests.exceptions import RequestException
from app import db, create_app
from app.models.Atractivo import Atractivo

class APIError(Exception):
    pass

class APIClient:
    def __init__(self):
        self.app = create_app()
        self.url = self.app.config['API_ATRACTIVOS_URL']
        self.timeout = self.app.config['API_TIMEOUT']

    def obtener_datos(self, limite=1000):
        try:
            response = requests.get(
                self.url, 
                params={'$limit': limite},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise APIError("Tiempo de espera agotado al consultar la API")
    
    def cargar_datos_iniciales(self):
        try:
            with self.app.app_context():
                datos = self.obtener_datos()
                
                if not datos:
                    raise APIError("No se obtuvieron datos de la API")

                for dato in datos:
                    atractivo = Atractivo(
                        municipio=dato.get('municipio', 'No especificado'),
                        tipo_de_atractivo=dato.get('tipo_de_atractivo', 'No especificado'),
                        subregion=dato.get('subregion', 'No especificada'),
                        nombre=dato.get('nombre', 'Sin nombre'),
                        ubicacion=dato.get('ubicacion', 'No especificada'),
                        descripcion=dato.get('descripcion', 'Sin descripción')
                    )
                    db.session.add(atractivo)
                
                db.session.commit()
                return True
                
        except Exception as e:
            db.session.rollback()
            raise APIError(f"Error al cargar datos iniciales: {str(e)}")