# Centi_Salud API 🩺

**Proyecto de Gestión de Personal Médico** *Desarrollo de API REST con FastAPI y MySQL*

---

## 👤 Información del Estudiante
* **Nombre y Apellidos:** Antonio David
* **Número de Alumno / ID:** 
* **GitHub:** [github.com/tu-usuario](https://github.com/antoniodavid13)

---

## 📝 Descripción del Proyecto
Este proyecto consiste en una **API REST desacoplada** diseñada para la gestión integral de registros médicos en el sistema **Centi_Salud**. 

La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar y Borrar) sobre una base de datos de especialistas. Se ha puesto especial énfasis en la **validación de datos** mediante Pydantic y en la **seguridad de la configuración** a través de variables de entorno, asegurando que el acceso a la base de datos MySQL sea robusto y escalable.

---

## 🛠️ Tecnologías Utilizadas
* **Framework:** FastAPI
* **Base de Datos:** MySQL
* **Validación:** Pydantic (Modelos y Validators)
* **Entorno:** Python-dotenv para gestión de `.env`

---

## ⚡ Instrucciones Básicas de Ejecución

Sigue estos pasos para poner en marcha la API en tu entorno local:

### 1. Configuración de la Base de Datos
Asegúrate de tener un servidor MySQL corriendo y ejecuta el siguiente script para preparar la estructura:

```sql
CREATE DATABASE cenit_salud_db;
USE cenit_salud_db;

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50) DEFAULT 'General',
    correo_interno VARCHAR(100) NOT NULL
);
