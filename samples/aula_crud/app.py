from flask import Flask, jsonify, request
from models.task import Task

app = Flask(__name__)

# CRUD

tasks = []
task_id_control = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(
        id=task_id_control, title=data["title"], description=data.get("description", "")
    )
    task_id_control += 1
    tasks.append(new_task)
    print(data)
    return jsonify({"message": "Tarefa criada com sucesso!", "data": data})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    # task_list = []
    # for task in tasks:
    #     task_list.append(task.to_dict())

    task_list = [task.to_dict() for task in tasks]

    output = {"tasks": task_list, "total_tasks": len(task_list)}
    return output


# Sobre o uso do <int:id> https://flask.palletsprojects.com/en/stable/quickstart/#variable-rules
@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = None
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return (
        jsonify({"message": f"Não foi possível encontrar a atividade com o id {id}"}),
        404,
    )


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return (
            jsonify(
                {"message": f"Não foi possível encontrar a atividade com o id {id}"}
            ),
            404,
        )

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]

    return jsonify({"message": "Tarefa atualizada com sucesso!", "data": data})
    # recomendado não indicar o status 200, pois já é o padrão


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return (
            jsonify(
                {"message": f"Não foi possível encontrar a atividade com o id {id}"}
            ),
            404,
        )

    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso!", "task": {"id": id}})


if __name__ == "__main__":
    app.run(debug=True)
