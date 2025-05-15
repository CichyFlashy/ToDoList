from flask import Flask, jsonify
import datetime

app = Flask(__name__)

class ToDo:
    def __init__(self, id, name, description, date):
        self.id = id
        self.name = name
        self.description = description
        self.date = datetime.now()

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
    return jsonify([todo.to_dict for todo in todos]) 

if __name__ == "__main__":
    app.run()