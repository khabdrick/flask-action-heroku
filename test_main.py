from main import db, app, TodoList
import json
import unittest

TEST_DB = "app_test.db"


class RecipesApiTests(unittest.TestCase):

    # executed before each test run
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app_test.db"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.create_todo()
        self.assertEqual(app.debug, False)

    def create_todo(self):
        item1 = TodoList(todo="Go to school")
        item2 = TodoList(todo="Make Mediterranean Chicken")

        db.session.add(item1)
        db.session.add(item2)

        db.session.commit()

    def test_todo_list_endpoint(self):

        response = self.app.get("/")
        # print (response.data)
        self.assertEqual(
            response.data,
            b'[{"id":1,"todo":"Go to school"},{"id":2,"todo":"Make Mediterranean Chicken"}]\n',
        )
        self.assertEqual(response.status_code, 200)

    def test_todo_creation_endpoint(self):
        json_data = {"todo": "Go to kschool"}
        response = self.app.post("/todo-create", data=json.dumps(json_data))
        # print(response.data)

        self.assertEqual(response.data, b'{"201":"todo created successfully"}\n')

    def test_update_todo_endpoint(self):

        json_data = {"todo": "just an update"}
        response = self.app.put(
            "/update/1",
            data=json.dumps(json_data),
            #  follow_redirects=True
        )

        self.assertEqual(response.data, b'{"200":"Updated successfully"}\n')

    # executed after each test
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
