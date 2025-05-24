from faker import Faker
from faker.providers import person

faker = Faker("pt_BR")
faker.add_provider(person)

def test_login_success(client):
    response = client.post("/login", json={
        "email": "admin@admin.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "Autenticação realizada com sucesso!" in json_data["message"]


def test_login_failure(client):
    response = client.post("/login", json={
        "email": "admin@admin.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    json_data = response.get_json()
    assert "Usuário não encontrado ou credenciais inválidas!" in json_data["message"]


def test_create_user(client):
    client.post("/login", json={
        "email": "admin@admin.com",
        "password": "admin123"
    })
    cpf = faker.cpf()
    response = client.post("/user", json={
        "username": "user_test",
        "cpf": cpf,
        "email": "user1@example.com",
        "password": "123456"
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert "Usuário criado com sucesso!" in json_data["message"]


def test_create_user_missing_fields(client):
    client.post("/login", json={
        "email": "admin@admin.com",
        "password": "admin123"
    })

    response = client.post("/user", json={
        "username": "user_test"
    })
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Campos obrigatórios ausentes" in json_data["message"]
