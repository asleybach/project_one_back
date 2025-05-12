# FinanzasPersonalesBack

**FinanzasPersonalesBack** es una API backend construida con **FastAPI** diseñada para gestionar ingresos y gastos personales. Proporciona autenticación segura basada en JWT, conexión a una base de datos PostgreSQL y un sistema modular para manejar usuarios, ingresos y gastos.

## Características

- **Gestión de ingresos y gastos**: Registra, actualiza, elimina y consulta ingresos y gastos personales.
- **Autenticación JWT**: Inicio de sesión y registro de usuarios con tokens JWT para garantizar la seguridad.
- **Conexión a PostgreSQL**: Almacenamiento de datos en una base de datos relacional robusta.
- **Estructura modular**: Código organizado en módulos para facilitar la escalabilidad y el mantenimiento.
- **Validación de datos**: Uso de Pydantic para garantizar la integridad de los datos enviados y recibidos.
- **Documentación interactiva**: Acceso a la documentación de la API mediante Swagger y ReDoc.

---

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y configurado
- Entorno virtual (opcional, pero recomendado)

---

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/finanzaspersonalesback.git
   cd finanzaspersonalesback
   ```

2. **Crea un entorno virtual** (opcional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
   ```env
   APP_NAME=FinanzasPersonalesBack
   APP_ENV=development
   APP_DEBUG=True
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=finanzas_db
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   SECRET_KEY=tu_clave_secreta
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

---

## Ejecución del proyecto

1. **Inicia el servidor**:
   Usa `uvicorn` para iniciar el servidor FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

2. **Accede a la API**:
   - Documentación interactiva de Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Documentación alternativa con ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Funcionalidades principales

### Autenticación
- **Registro de usuarios**: Crea una cuenta con un correo electrónico y contraseña.
- **Inicio de sesión**: Obtén un token JWT para acceder a las funcionalidades protegidas.

### Gestión de ingresos
- **Registrar ingresos**: Agrega ingresos con detalles como fuente, monto, categoría y fecha.
- **Consultar ingresos**: Obtén una lista de todos los ingresos registrados por el usuario autenticado.
- **Actualizar ingresos**: Modifica los detalles de un ingreso existente.
- **Eliminar ingresos**: Elimina un ingreso específico.

### Gestión de gastos
- **Registrar gastos**: Agrega gastos con detalles como método de pago, monto, categoría y fecha.
- **Consultar gastos**: Obtén una lista de todos los gastos registrados por el usuario autenticado.
- **Actualizar gastos**: Modifica los detalles de un gasto existente.
- **Eliminar gastos**: Elimina un gasto específico.

---

## Notas adicionales

- Asegúrate de que PostgreSQL esté en ejecución y configurado correctamente.
- Si encuentras problemas con las dependencias, verifica que las versiones de las librerías sean compatibles con tu entorno.
- Este proyecto utiliza Alembic para manejar las migraciones de la base de datos. Las migraciones se ejecutan automáticamente al iniciar el servidor.

---

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m "Agrega nueva funcionalidad"`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.