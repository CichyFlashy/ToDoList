from flask import Flask
import datetime

app = Flask(__name__)

class ToDo:
    def __init__(self, id, name, description, date):
        self.id = id
        self.name = name
        self.description = description
        self.date = datetime.now()



if __name__ == "__main__":
    app.run()