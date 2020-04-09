import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}.format('localhost:5432',
        # self.database_name)

        self.database_path = 'postgres://aar92_22@localhost:5432/trivia_test'

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.previous_question = {
            'id': 9,
            'question': "What boxer's original name is Cassius Clay?",
            'answer': 'Muhammad Ali',
            'difficulty': 1,
            'category': 4
        }

        # Executed after reach test
    def tearDown(self):
        pass

    def test_show_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_fail_show_categories(self):
        res = self.client().get('/categoriesp')

        self.assertEqual(res.status_code, 404)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    def test_fail_get_questions(self):
        res = self.client().get('/questionsp')

        self.assertEqual(res.status_code, 404)

    # def test_delete_question(self):
        # res = self.client().delete('/questions/6')
        # data = json.loads(res.data)

        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)

    def test_fail_delete_question(self):
        res = self.client().delete('questions/325290983')

        self.assertEqual(res.status_code, 422)

    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 1)

    def test_fail_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_filter_by_categories(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 4)
        self.assertEqual(data['current_category'], 'Art')

    def test_fail_filter_by_categories(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_provide_questions_quizzes(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': self.previous_question,
            'quiz_category': {'id': 4, 'type': 'History'}
        })

        self.assertEqual(res.status_code, 200)

    def test_fail_provide_questions_quizzes(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': None,
            'quiz_category': None})

        self.assertEqual(res.status_code, 400)


# TODO Write at least one test for each test for successful
# operation and for expected errors.

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
