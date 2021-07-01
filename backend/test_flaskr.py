import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.newQuestion ={
             'question': 'This is a question for testing',
             'answer': 'This is an answer', 
             'difficulty': 5,
             'category': 4
              }

        
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_paginated_questions(self):
        """Tests question pagination success"""

        res = self.client().get('/questions') 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_404_sent_requesting_beyond_vaid_page(self):
        """Tests question pagination failure 404"""

        res = self.client().get('/questions?page=9000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")


    def test_post_new_question(self):
        """Tests question creation success"""

        totalQuestions_before = len(Question.query.all())
        res = self.client().post('/questions' , json = self.newQuestion)
        data = json.loads(res.data)
        totalQuestions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(totalQuestions_after, totalQuestions_before + 1)


    def test_delete_question(self):
        """Tests question deletion success"""

        question = Question(question=self.newQuestion['question'], answer=self.newQuestion['answer'],category=self.newQuestion['category'], difficulty=self.newQuestion['difficulty'])
        question.insert()

        question_ID =question.id

        totalQuestions_before = len(Question.query.all())
        res = self.client().delete('/questions/{}'.format(question_ID))
        data = json.loads(res.data)
        totalQuestions_after = len(Question.query.all())

        question = Question.query.filter(Question.id == question_ID ).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_ID)
        self.assertEqual(totalQuestions_after, totalQuestions_before - 1)


    def test_422_Unprocessable_question_creation(self):
        """Tests question creation failure 422"""

        newQuestion ={
             'question': None,
             'answer': 'This is an answer', 
             'difficulty': 5,
             'category': 4
              }

        totalQuestions_before = len(Question.query.all())
        res = self.client().post('/questions' , json = newQuestion)
        data = json.loads(res.data)
        totalQuestions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(totalQuestions_after, totalQuestions_before)


    def test_successfull_search(self):
        """Tests search questions success"""

        res = self.client().post('/questions' , json = {'searchTerm':"movie"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'][0]['id'], 2)


    def test_404_search(self):
        """Tests search questions failure 404"""

        res = self.client().post('/questions' , json = {'searchTerm':"kkkkkkk"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_play_quiz(self):
        """Tests playing quiz game success"""

        res = self.client().post('/quizzes' , json ={'previous_questions': [20, 21],'quiz_category': {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['id'], 22)


    def test_422_play_quiz(self):
        """Tests playing quiz game failure 422"""

        res = self.client().post('/quizzes' , json ={'previous_questions': [20, 21 ,22 ,1 ,5],'quiz_category': {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
