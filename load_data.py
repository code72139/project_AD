from app import create_app
from app.services import APIClient

def cargar_datos():
    app = create_app()
    with app.app_context():
        cliente = APIClient()
        try:
            cliente.cargar_datos_iniciales()
            print("Datos cargados correctamente.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")

if __name__ == '__main__':
    cargar_datos()
