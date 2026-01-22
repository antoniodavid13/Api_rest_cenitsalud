from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict

# Carga las variables de entorno desde el archivo .env para proteger credenciales
load_dotenv(find_dotenv())

def get_connection():
    """
    Establece una conexión con la base de datos MySQL utilizando
    las variables de entorno configuradas.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "cenit_salud_db"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

def fetch_all_medicos() -> List[Dict[str, Any]]:
    """
    Recupera todos los registros de la tabla medicos.
    Retorna una lista de diccionarios donde cada clave es el nombre de la columna.
    """
    conn = None
    try:
        conn = get_connection()
        # dictionary=True permite que los resultados se mapeen como {columna: valor}
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]

        try:
            cur.execute("SELECT id_medico, nombre, especialidad, correo_interno FROM medicos;")
            # cast ayuda al linter de Python a entender que el retorno es una lista de dicts
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def insert_medico(nombre: str, especialidad: str, correo_interno: str | None) -> int:
    """
    Inserta un nuevo médico y devuelve el ID generado automáticamente.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Uso de placeholders (%s) para prevenir ataques de SQL Injection
            query = "INSERT INTO medicos (nombre, especialidad, correo_interno) VALUES (%s, %s, %s)"
            cur.execute(query, (nombre, especialidad, correo_interno))
            conn.commit()  # Confirma los cambios en la BD
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_medico(medico_id: int) -> bool:
    """
    Elimina un médico por su ID.
    Retorna True si al menos una fila fue afectada (eliminada).
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM medicos WHERE id_medico = %s", (medico_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_medico_by_id(medico_id: int) -> Dict[str, Any] | None:
    """
    Busca un médico específico. 
    Retorna un diccionario con sus datos o None si no existe.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]

        try:
            query = "SELECT id_medico, nombre, especialidad, correo_interno FROM medicos WHERE id_medico = %s"
            cur.execute(query, (medico_id,))
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def update_medico(medico_id: int, nombre: str, especialidad: str, correo_interno: str | None) -> bool:
    """
    Actualiza los campos de un médico.
    Retorna True si la actualización fue exitosa.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            query = """
                UPDATE medicos 
                SET nombre = %s, especialidad = %s, correo_interno = %s 
                WHERE id_medico = %s
            """
            cur.execute(query, (nombre, especialidad, correo_interno, medico_id))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()