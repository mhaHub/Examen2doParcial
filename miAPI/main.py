from fastapi import FastAPI, HTTPException, Depends, status
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets 
from datetime import date 


app= FastAPI(title="Examen2doParcial", description="Se tiene que pasar", version="1.0")

security = HTTPBasic()


citas = [
    {"id": 1,"nombre":"Andres", "Fecha": "11/12/2026","motivo":"Dolor de estomago"},
    {"id": 2,"nombre":"Diego", "Fecha": "1/06/2026","motivo":"Dolor de cabeza"},
    {"id": 3,"nombre":"Jack", "Fecha": "5/11/2026","motivo":"Dolor de espalada"}
]


def verificar_Peticion(credentials:HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username,"root")
    contraAuth = secrets.compare_digest(credentials.password,"1234")
    
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales no validas"
        )
        
    return credentials.username

class Citas(BaseModel):
    id : int = Field(...,gt=0,description="Identificadir de la cita")
    nombre: str = Field(..., min_length=5,description="Datos del paciente")
    fecha : date = Field(..., min_length=5,description="Datos del paciente")
    motivo: str = Field(...,max_length=100,description="Describir porque sucedio")


@app.get("/", tags=["Inicio"])
async def inicio():
    return {"mensaje": "Hola API"}

@app.get("/v1/citas/",tags=['CRUD CITAS'])
async def listarCitas(usuario_Auth:str= Depends(verificar_Peticion)):
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
async def eliminarCitas(id:int, usuario_Auth:str= Depends(verificar_Peticion)):
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
    
