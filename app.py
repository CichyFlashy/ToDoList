from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date
        }

todos = []

@app.route("/tasks", methods=['GET'])
def get_tasks():
    return jsonify([todo.to_dict() for todo in todos]) 

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    new_id = max([todo.id for todo in todos])+1 if todos else 1
    new_task = ToDo(
        id = new_id,
        name = data["name"],
        description = data["description"]

    )
    todos.append(new_task)
    return jsonify(new_task.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for todo in todos:
        if todo.id == task_id:
            todo.name = data.get('name', todo.name)
            todo.description = data.get('description', todo.description)
            todo.date = data.get('date', todo.date)
            return jsonify(todo.to_dict())
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    global todos

    task_to_delete = next((todo for todo in todos if todo.id == task_id), None)

    if task_to_delete is None:
        return jsonify({"error": "Zadanie nie znalezione"}), 404

    todos = [todo for todo in todos if todo.id != task_id]
    return '', 204

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()