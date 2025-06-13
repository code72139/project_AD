# Proyecto de Consumo de API - Atractivos Turísticos del Atlántico
![Demo](/project_AD.gif)

## Descripción
Este proyecto es una aplicación web que permite explorar y gestionar información sobre atractivos turísticos del departamento del Atlántico. La aplicación consume datos de una API pública y permite a los usuarios interactuar con la información mediante operaciones CRUD.

## Requisitos del Sistema
- Python 3.10 o superior
- PostgreSQL 12 o superior
- Git
- Navegador web

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/code72139/project_AD
cd project_AD
```

### 2. Configurar el Entorno Virtual
```bash

python -m venv .venv
source .venv/Scripts/activate

```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
DB_USER= tu_usuario
DB_PASSWORD= tu_contraseña
DB_HOST= localhost
DB_NAME= atractivos_turisticos
FLASK_DEBUG= 1
API_ATRACTIVOS_URL= https://www.datos.gov.co/resource/2fsd-7enq.json
API_TIMEOUT= 30
```

### 5. Crear la Base de Datos
Antes de ejecutar la aplicación, debes crear la base de datos en PostgreSQL:
```sql
CREATE DATABASE atractivos_turisticos;
```

### 6. Inicializar la Base de Datos
Crear las tablas necesarias en la base de datos:
```bash
python init_db.py
```

### 7. Cargar Datos Iniciales
Cargar los datos de atractivos turísticos desde la API:
```bash
python load_data.py
```

### 8. Ejecutar la Aplicación
```bash
python run.py
```
La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto
```
project_AD/
├── app/
│   ├── controllers/    # Controladores de la aplicación
│   ├── models/        # Modelos de la base de datos
│   ├── services/      # Servicios y lógica de negocio
│   ├── static/        # Archivos estáticos (CSS, JS)
│   ├── templates/     # Plantillas HTML
│   ├── __init__.py    # Inicialización de la aplicación
│   └── config.py      # Configuración de la aplicación
├── test/              # Pruebas unitarias
├── .env              # Variables de entorno
├── requirements.txt  # Dependencias del proyecto
├── init_db.py       # Script de inicialización de la BD
├── load_data.py     # Script de carga de datos
└── run.py           # Punto de entrada de la aplicación
```

## Pruebas Unitarias
El proyecto incluye pruebas unitarias para el servicio de favoritos. Las pruebas se encuentran en `test/test_favorito_service.py` y cubren las siguientes funcionalidades:

### Funcionalidades Probadas
- Agregar un atractivo a favoritos
- Manejo de errores al agregar favoritos (usuario no existe)
- Eliminar un atractivo de favoritos
- Manejo de errores al eliminar favoritos (favorito no existe, ID inválido)

### Ejecutar las Pruebas
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas con detalle
pytest -v

# Ejecutar pruebas específicas del servicio de favoritos
pytest test/test_favorito_service.py
```

### Estructura de Pruebas
- `test/`: Directorio principal de pruebas
  - `test_favorito_service.py`: Pruebas del servicio de favoritos
  - `conftest.py`: Configuración de pruebas (fixtures)
  - `__init__.py`: Archivo de inicialización

## Solución de Problemas Comunes

### Error de Conexión a la Base de Datos
- Verificar que PostgreSQL esté en ejecución
- Confirmar las credenciales en el archivo `.env`
- Asegurar que la base de datos existe

### Errores de Dependencias
- Actualizar pip: `python -m pip install --upgrade pip`
- Reinstalar dependencias: `pip install -r requirements.txt --force-reinstall`

### Problemas con el Entorno Virtual
- Eliminar el entorno virtual existente
- Crear un nuevo entorno virtual
- Reinstalar las dependencias

## Estructura del Dataset

### Atractivos o Productos Turísticos del departamento del Atlántico

- **Link:**  
  [Atractivos o Productos Turísticos](https://www.datos.gov.co/Comercio-Industria-y-Turismo/Atractivos-o-Productos-Tur-sticos-del-departamento/2fsd-7enq/about_data)

- **API:**  
  [Atractivos API](https://www.datos.gov.co/resource/2fsd-7enq.json)

En este conjunto de datos es posible encontrar Atractivos turísticos y diferentes productos (ferias, festivales, etc.) por municipios del departamento del Atlántico.

Los datos obtenidos desde la API contienen 225 filas y 6 columnas con la siguiente estructura:

- **municipio (texto):** Nombre del municipio donde está el atractivo.
- **tipo_de_atractivo (texto):** Clasificación general (ej: playa, feria, parque, etc.).
- **subregion (texto):** Subregión dentro del Atlántico (agrupación territorial).
- **atractivo_turistico_o_producto (texto):** Nombre del lugar o evento (ej: Carnaval de Barranquilla).
- **lugar_de_ubicacion (texto):** Dirección, sitio exacto o localidad.
- **descripcion (texto):** Breve resumen o explicación del atractivo.

### Funcionalidades Principales

- **Página de Inicio:** Muestra una lista de atractivos turísticos.
- **Favoritos:** Permite a los usuarios ver los atractivos guardados como favoritos.
- **Comentarios:** Los usuarios pueden escribir en cada uno de los atractivos.
- **Gestión CRUD:** Crear, leer, actualizar y eliminar información relacionada con los requerimientos de la aplicación.

