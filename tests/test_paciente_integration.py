
def test_healthcheck(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_crear_y_consultar_por_id(client):
    payload = {"nombre": "Ana", "edad": 30, "historia_clinica": "Alergia a penicilina"}
    r = client.post("/pacientes", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert "id" in data and isinstance(data["id"], int)
    assert data["nombre"] == payload["nombre"]
    assert data["edad"] == payload["edad"]
    assert data["historia_clinica"] == payload["historia_clinica"]
    pid = data["id"]

    r2 = client.get(f"/pacientes/{pid}")
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["nombre"] == "Ana"
    assert d2["edad"] == 30
    assert d2["historia_clinica"] == "Alergia a penicilina"

def test_eliminar_y_404_luego(client):
    payload = {"nombre": "Luis", "edad": 40, "historia_clinica": "Hipertensión"}
    r = client.post("/pacientes", json=payload)
    pid = r.json()["id"]

    r_del = client.delete(f"/pacientes/{pid}")
    assert r_del.status_code == 204

    r_get = client.get(f"/pacientes/{pid}")
    assert r_get.status_code == 404

def test_eliminar_inexistente_retorna_404(client):
    r = client.delete("/pacientes/9999")
    assert r.status_code == 404
