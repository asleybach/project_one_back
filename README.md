# BaseBackFastAPI

BaseBackFastAPI es una API backend construida con **FastAPI** que incluye autenticación basada en JWT, conexión a una base de datos PostgreSQL y un sistema modular para manejar usuarios y autenticación.

## Características

- **Autenticación JWT**: Inicio de sesión y registro de usuarios con tokens JWT.
- **Conexión a PostgreSQL**: Gestión de usuarios almacenados en una base de datos PostgreSQL.
- **Estructura modular**: Código organizado en módulos para facilitar la escalabilidad.
- **Validación de datos**: Uso de Pydantic para validar entradas y salidas.

---

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y configurado
- Entorno virtual (opcional, pero recomendado)

---

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/basebackfastapi.git
   cd basebackfastapi

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


## Ejecución del proyecto

1. **Inicia el servidor**:
   Usa `uvicorn` para iniciar el servidor FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

2. **Accede a la API**:
   - Documentación interactiva de Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   



## Notas adicionales

- Asegúrate de que PostgreSQL esté en ejecución y configurado correctamente.
- Si encuentras problemas con las dependencias, verifica que las versiones de las librerías sean compatibles con tu entorno.