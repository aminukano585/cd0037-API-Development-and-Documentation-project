import os
from dotenv import load_dotenv
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

from flaskr import create_app
from models import setup_db, Question, Category

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'trivia_test')
TEST_DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, TEST_DB_NAME)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = TEST_DB_PATH
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
    def test_read_all_categories(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_read_all_categories_not_allowed(self):
        res = self.client().delete('/api/v1.0/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not allowed')

    def test_read_questions(self):
        res = self.client().get('/api/v1.0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_read_questions_bad_request(self):
        res = self.client().get('/api/v1.0/questions?page=5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_delete_question(self):
        question_id = Question.query.first().format()['id']
        res = self.client().delete('/api/v1.0/questions/' + str(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_not_found(self):
        res = self.client().delete('/api/v1.0/questions/weird-id')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_create_question(self):
        new_question = {
            'question': 'Who are you?', 'answer': 'Human', 'category': 1, 'difficulty': 1
        }
        res = self.client().post('/api/v1.0/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created']['answer'], 'Human')

    def test_create_question_unprocessable_resource(self):
        res = self.client().post('/api/v1.0/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable resource')

    def test_search_question(self):
        res = self.client().post('/api/v1.0/questions', json={"searchTerm": "title"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_search_question_bad_request(self):
        res = self.client().post('/api/v1.0/questions', json={"searchTerm": "~!@"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_read_questions_in_category(self):
        category_id = Category.query.first().format()['id']
        res = self.client().get('/api/v1.0/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category_id)

    def test_read_questions_in_category_not_found(self):
        res = self.client().get('/api/v1.0/categories/12928/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_quiz_question(self):
        category = Category.query.first()
        res = self.client().post('/api/v1.0/quizzes', json={"quiz_category": category.format()})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_quiz_question_unprocessable_resource(self):
        res = self.client().post('/api/v1.0/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable resource')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()