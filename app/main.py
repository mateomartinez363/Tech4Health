from fastapi import Depends, FastAPI, HTTPException
from typing import Optional,List
from app.db import Base, engine, get_db
from app.models import Paciente
from sqlalchemy.orm import Session
from app import models
from app.schemas import CrearPaciente, LeerPaciente

app = FastAPI(title = "Tech4Health API")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/pacientes", response_model=LeerPaciente, status_code=201)
def crear_paciente(data: CrearPaciente, db: Session = Depends (get_db)):
    nuevo_paciente = Paciente(
        nombre=data.nombre,
        edad=data.edad,
        historia_clinica=data.historia_clinica
    )
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente

@app.get("/pacientes/{paciente_id}", response_model=LeerPaciente)
def devovler_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.get(Paciente, paciente_id)
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@app.delete("/pacientes/{paciente_id}", status_code=204)
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.get(Paciente, paciente_id)

    if not paciente:
        raise HTTPException(status_code=404, detail = "Paciente no encontrado")
    db.delete(paciente)
    db.commit()

    return
