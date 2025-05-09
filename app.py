from app.services.api_service import APIClient

cliente = APIClient()
datos = cliente.obtener_datos()
if datos:
      for item in datos:
          print(item)