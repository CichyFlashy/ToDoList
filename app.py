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

@app.route("/tasks", methods=['GET'])
def get_tasks():
    todos = ToDo.query.all()
    return jsonify([todo.to_dict() for todo in todos]) 

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = ToDo(name=data["name"], description=data["description"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    todo = ToDo.query.get(task_id)
    if not todo:
        return jsonify({"error": "Task not found"}), 404

    todo.name = data.get('name', todo.name)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    todo = ToDo.query.get(task_id)
    if not todo:
        return jsonify({"error": "Zadanie nie znalezione"}), 404

    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()