from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy

# instantiate Flask functionality
app = Flask(__name__)

# set sqlalchemy URI in application config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)  # instance of SQL


class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"{self.id} {self.todo}"


def todo_serializer(todo):
    # convert data from TodoList to JSON
    return {"id": todo.id, "todo": todo.todo}


@app.route("/", methods=["GET"])
def home():
    return jsonify([*map(todo_serializer, TodoList.query.all())])


@app.route("/todo-create", methods=["POST"])
def todo_create():
    # add todo to database
    request_data = json.loads(request.data)
    todo = TodoList(todo=request_data["todo"])

    db.session.add(todo)
    db.session.commit()

    return {"201": "todo created successfully"}


@app.route("/update/<int:id>", methods=["PUT"])
def update_todo(id):
    # edit todo item based on ID
    item = TodoList.query.get(id)
    request.get_json(force=True)
    todo = request.json["todo"]
    item.todo = todo
    db.session.commit()

    return {"200": "Updated successfully"}


@app.route("/<int:id>", methods=["POST"])
def delete_todo(id):
    # delete todo item from todo list
    request.get_json(force=True)
    request_data = json.loads(request.data)

    TodoList.query.filter_by(id=request_data["id"]).delete()
    db.session.commit()
    return {"204": "Delete successfully"}


if __name__ == "__main__":
    app.run(debug=True)
