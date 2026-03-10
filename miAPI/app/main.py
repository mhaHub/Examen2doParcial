from fastapi import FastApi, HTTPException
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials


app = FastApi(title="Examen2doParcial", description="Se tiene que pasar", version="2.0")

security = HTTPBasic()


citas = [
    {"id": 1,"nombre":"Andres", "Fecha": "11/12/2026","motivo":"Dolor de estomago"},
    {"id": 2,"nombre":"Andres", "Fecha": "1/06/2026","motivo":"Dolor de cabeza"},
    {"id": 3,"nombre":"Andres", "Fecha": "5/11/2026","motivo":"Dolor de espalada"}
]

class Citas(BaseModel):
    id : int = Field(...,gt=0,description="Identificadir de la cita")
    nombre: str = Field(..., min_length=5,description="Datos del paciente")
    fecha: int = Field(...,le="09/03/2026")
    motivo: str = Field(...,max_length=100,description="Describir porque sucedio")
    

@app.get("/v1/citas/",tags=['CRUD CITAS'])
async def listarCitas():
    return{
        "status": 200,
        "total": len(citas),
        "data": citas
    }
    
@app.get("/v1/citas/{id}",tags=['CRUD CITAS'])
async def consultasID(id:int):
    return{
        "Cita encontrada": id
    }
    
@app.post("/v1/citas/",tags=['CRUD CITAS'])
async def agregarCita(id:int, citas:Citas):
    for cta in citas:
        if cta["id"] == citas.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    citas.append(citas.dict())
    
    return {
        "mensaje": "Cita agregada correctamente"
    }
@app.delete("/v1/citas/{id}",tags=['CRUD CITAS'])
async def eliminarCitas(id:int):
    for cta in citas:
        if cta["id"] == citas.id:
            citas.remove(cta)
            return{
                "mensaje": "Cita Eliminada"
            }
    raise HTTPException(
        status_code=400,
        detail="La cita no existe"
    )
    
