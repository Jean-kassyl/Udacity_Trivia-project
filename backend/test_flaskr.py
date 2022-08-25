import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

from flaskr import create_app
from models import setup_db, Question, Category


db_password = os.getenv("PASSWORD")
db_name = os.getenv("DBNAME")

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(f'{db_name}:{db_password}@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/trivia/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_categories_failure(self):
        res = self.client().get('/trivia/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_paginated_questions_list(self):
        res = self.client().get('/trivia/questions')
        data = json.loads(res.data)

        q = Question.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data['total_questions'], len(q))
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])

    def test_paginated_questions_outOfRange(self):
        res = self.client().get('/trivia/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data["message"], "Not found")

    def test_delete_question(self):
        res = self.client().delete('/trivia/questions/2') #make sure the id exists in the trivia_test database
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2) # make sure the id is the as the one above

    def test_delete_not_processed(self):
        res = self.client().delete('/trivia/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        res = self.client().post('/trivia/questions', json={"question": "who is the actor that played the role of batman in year 2021", "answer": "Robert Pattinson", "difficulty": "2", "category": "5"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])

    def test_badRequest_error_creating_question(self):
        res = self.client().post('/trivia/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "Bad request")

    def test_error_creating_question(self):
        res = self.client().post('/trivia/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_questions(self):
        res = self.client().post('/trivia/questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_search_questions_failure(self):
        res = self.client().post('/trivia/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "Bad request")

    def test_get_questions_basedOn_category(self):
        res = self.client().get('/trivia/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])

    def test_get_questions_basedOn_category_failure(self):
        res = self.client().get('/trivia/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["error"], 404)


    def test_get_question_for_quiz(self):
        res = self.client().post('/trivia/quizzes', json={"previous_questions": [2, 19], "quiz_category": {"type": "", "id": 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])

    def test_get_question_for_quiz_failure(self):
        res = self.client().post('/trivia/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['error'], 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()