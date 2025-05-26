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
   source .venv/bin/activate  
   .venv\Scripts\activate    
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

## Migraciones de Base de Datos

Este proyecto utiliza **Alembic** para gestionar las migraciones de la base de datos.  
**Importante:**  
> Los cambios realizados en los modelos de SQLAlchemy (por ejemplo, agregar o eliminar columnas) **no se aplican automáticamente** en la base de datos.  
> Es necesario crear y aplicar migraciones manualmente para reflejar estos cambios en la estructura de la base de datos.

### ¿Cómo crear y aplicar una migración?

1. **Realiza los cambios en tus modelos** (por ejemplo, en `models/income.py`).
2. **Genera una nueva migración Alembic** ejecutando:
   ```bash
   alembic revision --autogenerate -m "Describe tu cambio"
   ```
   Esto creará un nuevo archivo de migración en la carpeta `alembic/versions/`.
3. **Aplica la migración**:
   ```bash
   alembic upgrade head
   ```
   Si tu aplicación ejecuta `alembic upgrade head` al iniciar, la migración se aplicará automáticamente en el próximo arranque.

### Notas

- Si solo modificas los modelos y no generas/aplicas la migración, los cambios **no se verán reflejados** en la base de datos.
- Puedes revisar la carpeta `alembic/versions/` para ver el historial de migraciones aplicadas.
- Consulta la [documentación oficial de Alembic](https://alembic.sqlalchemy.org/en/latest/) para más detalles y buenas prácticas.

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