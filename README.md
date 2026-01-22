Este es un README.md profesional y completo para tu proyecto. He estructurado la información para que cualquier desarrollador (o tú mismo en el futuro) pueda entender cómo instalarlo, configurarlo y usarlo.

Markdown
# Centi_Salud API 🩺

API REST robusta desarrollada con **FastAPI** para la gestión de personal médico. Este proyecto implementa una arquitectura desacoplada, utilizando **Pydantic** para validación de esquemas y **MySQL** como motor de base de datos.

## 🚀 Características

* **Arquitectura en Capas:** Separación clara entre la lógica de negocio (API) y el acceso a datos (Database).
* **Validación Estricta:** Uso de Pydantic para asegurar la integridad de los datos de entrada y salida.
* **Seguridad:** Gestión de credenciales mediante variables de entorno (`.env`).
* **Documentación Interactiva:** Autogenerada con Swagger UI y Redoc.
* **Tipado Estático:** Implementación de `typing` para un código más legible y menos propenso a errores.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
* **Lenguaje:** Python 3.10+
* **Base de Datos:** MySQL

---

## 📋 Requisitos Previos

1.  Python instalado (v3.10 o superior).
2.  Servidor MySQL activo.
3.  Un archivo `.env` en la raíz del proyecto con el siguiente formato:

```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=cenit_salud_db
DB_PORT=3306
