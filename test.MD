# Tests para el Servicio de Favoritos

Este documento explica la estructura, configuración y propósito de los tests automatizados para el módulo de gestión de favoritos en la aplicación. Se detalla la configuración del entorno de pruebas, los fixtures utilizados y cada prueba implementada para validar el correcto funcionamiento del servicio `favorito_service`.

---

## 1. Configuración del entorno de pruebas (`tests/conftest.py`)

### Objetivo

Configurar un entorno aislado y controlado para la ejecución de pruebas automatizadas usando `pytest`, asegurando que cada test se ejecute en una base de datos limpia e independiente.

### Descripción de Fixtures

- **`app`**

  - Crea una instancia de la aplicación Flask en modo testing (`TESTING=True`).
  - Configura una base de datos en memoria SQLite para que los tests no afecten datos reales.
  - Inicializa el esquema de base de datos (`db.create_all()`).
  - Garantiza la limpieza del estado después de cada prueba mediante `db.session.remove()` y `db.drop_all()`.
  - Utiliza un contexto de aplicación para que los tests puedan usar el entorno de Flask y SQLAlchemy correctamente.

- **`db_session`**

  - Proporciona una sesión de base de datos SQLAlchemy vinculada a la app configurada en `app`.
  - Usada en cada test para operaciones CRUD sobre la base de datos.
  - Asegura que después de cada test se haga rollback para descartar cambios y mantener la base limpia.

- **`client`**
  - Proporciona un cliente de pruebas para realizar peticiones HTTP a la aplicación Flask.

---

## 2. Tests de `favorito_service`

### Objetivo

Verificar la correcta funcionalidad del servicio que permite agregar y eliminar favoritos, asegurando el manejo correcto de escenarios válidos e inválidos.

---

### 2.1 Test: `test_agregar_favorito`

- **Propósito:**
  Validar que se pueda agregar un favorito correctamente para un usuario y atractivo existentes.

- **Procedimiento:**

  1. Crear un usuario y un atractivo en la base de datos de prueba.
  2. Ejecutar la función `agregar_favorito` con el ID del atractivo y el usuario.
  3. Verificar que la respuesta sea exitosa (`status == "ok"`).
  4. Confirmar que el favorito creado tenga correctamente asignado el usuario y el atractivo.

- **Importancia:**
  Garantiza que la funcionalidad principal para crear favoritos funcione bajo condiciones normales.

---

### 2.2 Test: `test_agregar_favorito_usuario_no_existe`

- **Propósito:**
  Verificar que el servicio maneje correctamente la situación cuando se intenta agregar un favorito para un usuario que no existe.

- **Procedimiento:**

  1. Crear solo un atractivo en la base de datos.
  2. Intentar agregar un favorito con un `usuario_id` inexistente (ej. 9999).
  3. Confirmar que la respuesta sea de error (`status == "error"`).
  4. Validar que el mensaje de error sea informativo ("Usuario no encontrado").

- **Importancia:**
  Asegura que la aplicación maneje errores de integridad referencial y no permita crear favoritos inválidos.

---

### 2.3 Test: `test_eliminar_favorito_existe`

- **Propósito:**
  Confirmar que un favorito existente pueda ser eliminado correctamente.

- **Procedimiento:**

  1. Crear un usuario, un atractivo y un favorito asociado.
  2. Ejecutar la función `eliminar_favorito` con el ID del favorito creado.
  3. Verificar que la respuesta sea exitosa (`status == "ok"`).
  4. Comprobar que el favorito haya sido efectivamente eliminado de la base de datos.

- **Importancia:**
  Verifica la funcionalidad de borrado y que el sistema mantenga la consistencia tras eliminar datos.

---

### 2.4 Test: `test_eliminar_favorito_no_existe`

- **Propósito:**
  Verificar que intentar eliminar un favorito que no existe genere un error manejado.

- **Procedimiento:**

  1. Ejecutar `eliminar_favorito` con un ID que no corresponde a ningún favorito (ej. 9999).
  2. Confirmar que el resultado sea un error (`status == "error"`).
  3. Validar que el mensaje contenga la indicación "Favorito no encontrado".

- **Importancia:**
  Asegura que la función maneje adecuadamente entradas inválidas sin afectar la estabilidad.

---

### 2.5 Test: `test_eliminar_favorito_id_invalido`

- **Propósito:**
  Verificar la validación sobre el parámetro `id_favorito` cuando se pasa un valor inválido (ej. negativo).

- **Procedimiento:**

  1. Ejecutar `eliminar_favorito` con un ID inválido (-5).
  2. Comprobar que la respuesta sea de error.
  3. Verificar que el mensaje indique que el ID debe ser positivo.

- **Importancia:**
  Refuerza la validación de entrada para evitar operaciones erróneas o maliciosas.

---

## 3. Consideraciones finales

- Cada test es **independiente** y se ejecuta en una base de datos limpia gracias a la configuración de los fixtures.
- Se usa una base de datos SQLite en memoria para máxima velocidad y aislamiento.
- La estrategia garantiza que los tests no se afecten entre sí y que reflejen el comportamiento real esperado.
- Los mensajes de error son validados para asegurar buena comunicación de fallos y facilitar la depuración.
- Los fixtures proporcionan una forma flexible y reutilizable de preparar el estado necesario para las pruebas.
