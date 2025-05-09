# Detalle de Entregas

## Entrega 1 (9 de mayo)

**Objetivo:** Diseño inicial y configuración del proyecto.

**Requisitos:**
- Seleccionar un dataset de datos.gov.co.
- Documentar en README.md el objetivo del proyecto y estructura del dataset.
- Configurar el entorno Python (requirements.txt con dependencias).
- Implementar un cliente básico (APIClient) para consumir datos.
- Subir el repositorio en GitHub/GitLab con un commit inicial.

---

# Proyecto de Consumo de API

## Objetivo del Proyecto

Este proyecto tiene como objetivo consumir datos desde una API pública utilizando Python y almacenarlos en una base de datos SQL. Se hace uso de la librería `requests` para realizar la petición HTTP. El propósito es demostrar cómo se puede consumir datos externos para su posterior análisis o uso en otras aplicaciones.

Se plantea la posibilidad de una app web que permite explorar, filtrar y guardar atractivos turísticos del Atlántico, con funciones CRUD para agregar favoritos, notas personales, reseñas o comentarios por parte de los usuarios.

- **Create:** Guardar un atractivo como favorito.
- **Read:** Ver atractivos por categoría.
- **Update:** Agregar nota, comentario o calificación.
- **Delete:** Eliminar de favoritos.

---

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
