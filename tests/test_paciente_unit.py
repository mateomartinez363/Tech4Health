# tests/test_paciente_unit.py
import pytest
from pydantic import ValidationError

# Ajusta los imports a tu proyecto
from app.schemas import CrearPaciente, LeerPaciente
from app.models import Paciente  # SQLAlchemy


def test_schema_crear_valido():
    data = {"nombre": "Ana", "edad": 30, "historia_clinica": "Alergia a penicilina"}
    p = CrearPaciente(**data)
    assert p.nombre == "Ana"
    assert p.edad == 30
    assert p.historia_clinica.startswith("Alergia")


def test_schema_crear_invalido_falta_nombre():
    with pytest.raises(ValidationError):
        CrearPaciente(edad=25, historia_clinica="N/A")  # falta nombre


def test_schema_crear_invalido_tipos():
    with pytest.raises(ValidationError):
        CrearPaciente(
            nombre=123, edad="treinta", historia_clinica=[]
        )  # tipos incorrectos


def test_schema_leer_incluye_historia_clinica():
    # Simula un objeto ORM y valida que LeerPaciente expone la historia clínica
    orm = Paciente(id=1, nombre="Luis", edad=40, historia_clinica="Privado")
    out = LeerPaciente.model_validate(orm, from_attributes=True)
    assert out.id == 1
    assert out.nombre == "Luis"
    assert out.edad == 40
    assert out.historia_clinica == "Privado"


def test_model_patient_instancia_simple():
    p = Paciente(nombre="Sofía", edad=22, historia_clinica="Control anual")
    # Sin persistir en BD: validamos tipos/atributos básicos del modelo
    assert isinstance(p, Paciente)
    assert p.id is None  # aún no fue insertado
    assert p.nombre == "Sofía"
    assert p.edad == 22
