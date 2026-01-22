from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Annotated
from app.database import (
    fetch_all_medicos, 
    fetch_medico_by_id, 
    insert_medico, 
    update_medico, 
    delete_medico
)

# Configuración de la instancia principal de FastAPI
app = FastAPI(
    title="Centi_Salud API",
    version="1.0.0",
    description="API REST para la gestión integral de personal médico y especialistas"
)

# ========================
# Modelos de Datos (Schemas)
# ========================

class MedicoBase(BaseModel):
    """
    Esquema base que define los atributos comunes de un médico.
    Utiliza Annotated y Field para validaciones de longitud y valores por defecto.
    """
    nombre: Annotated[str, Field(min_length=1, max_length=50, description="Nombre completo del médico")]
    especialidad: Annotated[str, Field(default="General", min_length=1, max_length=50)]
    correo_interno: Annotated[str, Field(default="", min_length=1, max_length=100)]

    @field_validator('nombre', 'especialidad')
    @classmethod
    def validar_campos_texto(cls, v: str) -> str:
        """Asegura que los campos de texto no contengan solo espacios en blanco."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío ni contener solo espacios')
        return v.strip()

    @field_validator('correo_interno')
    @classmethod
    def validar_correo(cls, v: str) -> str:
        """Normaliza el correo electrónico a mayúsculas y valida que no esté vacío."""
        v = v.strip().upper()
        if not v:
            raise ValueError('El correo interno es obligatorio')
        return v

class MedicoCreate(MedicoBase):
    """Esquema para la creación de registros (no requiere ID)."""
    pass

class MedicoUpdate(MedicoBase):
    """Esquema para la actualización de registros."""
    pass

class Medico(MedicoBase):
    """Esquema completo que representa la entidad en la base de datos."""
    id_medico: int

# ========================
# Utilidades / Helpers
# ========================

def map_rows_to_medicos(rows: List[dict]) -> List[Medico]:
    """
    Convierte registros crudos de la base de datos (diccionarios) 
    en objetos validados por Pydantic (Modelo Medico).
    """
    return [Medico(**dict(row)) for row in rows]

# ========================
# Endpoints de la API
# ========================

@app.get("/ping", tags=["Salud del Sistema"])
def ping():
    """Verifica la disponibilidad del servicio."""
    return {"status": "online", "message": "pong"}

@app.get("/medicos", response_model=List[Medico], tags=["Médicos"])
def listar_medicos():
    """Obtiene la lista completa de médicos desde la base de datos."""
    rows = fetch_all_medicos()
    return map_rows_to_medicos(rows)

@app.get("/medicos/{medico_id}", response_model=Medico, tags=["Médicos"])
def obtener_medico(medico_id: int):
    """
    Busca un médico por su ID único.
    Retorna 404 si el registro no existe en la base de datos.
    """
    row = fetch_medico_by_id(medico_id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico con ID {medico_id} no encontrado"
        )
    
    return map_rows_to_medicos([row])[0]

@app.post("/medicos", response_model=Medico, status_code=status.HTTP_201_CREATED, tags=["Médicos"])
def crear_medico(medico: MedicoCreate):
    """
    Registra un nuevo médico.
    Realiza la inserción, valida el éxito y recupera el objeto creado.
    """
    nuevo_id = insert_medico(
        nombre=medico.nombre,
        especialidad=medico.especialidad,
        correo_interno=medico.correo_interno
    )
    
    if not nuevo_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error crítico al insertar el médico"
        )
    
    row = fetch_medico_by_id(nuevo_id)
    return map_rows_to_medicos([row])[0]

@app.put("/medicos/{medico_id}", response_model=Medico, tags=["Médicos"])
def actualizar_medico(medico_id: int, medico: MedicoUpdate):
    """
    Actualiza los datos de un médico existente.
    Verifica existencia previa antes de proceder con la actualización.
    """
    # Verificación de existencia
    if not fetch_medico_by_id(medico_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico con ID {medico_id} no encontrado"
        )
    
    actualizado = update_medico(
        medico_id=medico_id,
        nombre=medico.nombre,
        especialidad=medico.especialidad,
        correo_interno=medico.correo_interno
    )
    
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo procesar la actualización en la base de datos"
        )
    
    row_actualizado = fetch_medico_by_id(medico_id)
    return map_rows_to_medicos([row_actualizado])[0]

@app.delete("/medicos/{medico_id}", status_code=status.HTTP_200_OK, tags=["Médicos"])
def eliminar_medico(medico_id: int):
    """
    Elimina un registro médico de forma permanente.
    """
    if not fetch_medico_by_id(medico_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Médico con ID {medico_id} no encontrado"
        )
    
    if not delete_medico(medico_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al intentar eliminar el registro"
        )
    
    return {
        "mensaje": "Médico eliminado exitosamente",
        "id_medico": medico_id
    }