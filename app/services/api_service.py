import requests

url = "https://www.datos.gov.co/resource/2fsd-7enq.json"

class APIClient:
  
  def obtener_datos(self, limite=1000):
    response = requests.get(url, params={'$limit': limite})

    if response.status_code == 200:
        return response.json()
    else:
      print(f"Error al obtener datos: {response.status_code}")
      return None