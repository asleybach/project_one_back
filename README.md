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