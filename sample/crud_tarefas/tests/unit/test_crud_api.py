import pytest

from sample.crud_tarefas.src.app import app, tasks
from sample.crud_tarefas.src.models.task import Task


# CRUD
@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def setup_task():
    global task_id_control
    tasks.clear()
    task_id_control = 1

    task = Task(
        id=task_id_control,
        title="Tarefa Inicial",
        description="Descrição da tarefa inicial",
    )
    tasks.append(task)

    task_id_control += 1

    yield  # ponto de execução do teste

    tasks.clear()
    task_id_control = 1


# pytest -m "api" para executar somente os testes marcados como api
# @pytest.mark.usefixtures("setup_task") - já setado como autouse para todos os testes
class TestCrudTarefas:

    def test_create_task(self, client):
        new_task_data = {
            "title": "Nova Tarefa",
            "description": "Descrição da nova tarefa",
        }
        response = client.post("/tasks", json=new_task_data)
        assert response.status_code == 200, (
            f"Requisição POST retornou status_code {response.status_code}, "
            "mas o esperado era 200"
        )

        response_json = response.get_json()
        assert "message" in response_json, "Requisição não retornou a chave 'message'."
        assert (
            "data" in response_json
        ), "Requisição não retornou a chave 'data' com os dados da tarefa."
        assert "id" in response_json["data"], "Requisição não retornou a chave 'id'."

    def test_get_tasks(self, client):
        response = client.get("/tasks")
        assert response.status_code == 200, (
            f"Requisição GET tasks retornou status_code {response.status_code}, "
            "mas o esperado era 200"
        )

        response_json = response.get_json()
        assert (
            "tasks" in response_json
        ), "Requisição não retornou a chave 'tasks' com a lista de tarefas."
        assert "total_tasks" in response_json, (
            "Requisição não retornou a chave 'total_tasks' com o tamanho "
            "da lista de tarefas."
        )

    def test_get_task(self, client):
        id = 1
        response = client.get(f"/tasks/{id}")
        assert response.status_code == 200, (
            f"Requisição GET task retornou status_code {response.status_code}, "
            "mas o esperado era 200"
        )

        response_json = response.get_json()
        assert response_json["id"] == id, "Requisição não retornou a chave 'id'."

    def test_get_non_existent_task(self, client):
        id = 99999
        response = client.get(f"/tasks/{id}")
        assert response.status_code == 404, (
            f"Requisição GET task retornou status_code {response.status_code}, "
            "mas o esperado era 404"
        )

        response_json = response.get_json()
        assert "message" in response_json, "Requisição não retornou a chave 'message'."

    def test_put_task(self, client):
        id = 1
        updated_task_data = {
            "title": "Tarefa atualizada",
            "description": "Descrição da tarefa atualizada",
            "completed": True,
        }

        response = client.put(f"/tasks/{id}", json=updated_task_data)
        assert (
            response.status_code == 200
        ), "Requisição PUT task não retornou status_code 200."

        response_json = response.get_json()
        assert "message" in response_json, "Requisição não retornou a chave 'message'."
        assert (
            "data" in response_json
        ), "Requisição não retornou a chave 'data' com os dados da tarefa."
        assert response_json["data"]["id"] == id, (
            f"Requisição retornou a chave 'id' {response_json['data']['id']}, mas "
            f"o esperado era {id}"
        )
        assert response_json["data"]["title"] == updated_task_data["title"], (
            f"Requisição retornou a chave 'title' {response_json['data']['title']}, "
            f"mas o esperado era {updated_task_data['title']}"
        )
        assert (
            response_json["data"]["description"] == updated_task_data["description"]
        ), (
            f"Requisição retornou a chave 'description' "
            f"{response_json['data']['description']}, mas o esperado era "
            f"{updated_task_data['description']}"
        )
        assert response_json["data"]["completed"] == updated_task_data["completed"], (
            "Requisição retornou a chave 'completed' "
            f"{response_json['data']['completed']}, "
            f"mas o esperado era {updated_task_data['completed']}"
        )

    def test_put_non_existent_task(self, client):
        id = 99999
        updated_task_data = {
            "title": "Tarefa atualizada",
            "description": "Descrição da tarefa atualizada",
            "completed": True,
        }
        response = client.put(f"/tasks/{id}", json=updated_task_data)
        assert response.status_code == 404, (
            f"Requisição PUT task retornou status_code {response.status_code}, "
            "mas o esperado era 404"
        )

        response_json = response.get_json()
        assert "message" in response_json, "Requisição não retornou a chave 'message'."

    def test_delete_task(self, client):
        id = 1

        response = client.delete(f"/tasks/{id}")
        assert response.status_code == 200, (
            f"Requisição DELETE task retornou status_code {response.status_code}, "
            "mas o esperado era 200"
        )

        response_json = response.get_json()
        assert "message" in response_json, "Requisição não retornou a chave 'message'."
        assert "task" in response_json, (
            "Requisição não retornou a chave 'task', "
            "onde informa o 'id' da tarefa deletada."
        )
        assert (
            "id" in response_json["task"]
        ), "Requisição não retornou a chave 'id' com dado da tarefa deletada"
        assert response_json["task"]["id"] == id, (
            f"Requisição retornou a chave 'id' {response_json['task']['id']}, mas "
            f"o esperado era {id}"
        )

    def test_delete_non_existent_task(self, client):
        id = 99999
        response = client.delete(f"/tasks/{id}")
        assert response.status_code == 404, (
            f"Requisição DELETE task retornou status_code {response.status_code}, "
            "mas o esperado era 404"
        )

        response_json = response.get_json()
        assert "message" in response_json, "Requisição não retornou a chave 'message'."


# exemplo com happy e edge cases

# @pytest.mark.parametrize("valor, esperado", [
#     (0, "inválido"),
#     (-1, "inválido"),
#     (9999999, "inválido"),
#     ("", "inválido"),
# ])
# def test_edge_case_criacao(valor, esperado):
#     with pytest.raises(ValueError):
#         criar_tarefa(valor)
