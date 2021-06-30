import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
	'''
	 function for paginating questions
	'''
		page = request.args.get('page', 1, type=int)
		start = (page - 1) * QUESTIONS_PER_PAGE
		end = start + QUESTIONS_PER_PAGE

		questions = [question.format() for question in selection]
		current_questions = questions[start:end]

		return current_questions


def create_app(test_config=None):
	'''
	  create and configure the app
	'''
	app = Flask(__name__)
	setup_db(app)

	#Set up CORS. Allow '*'for origins
	cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
	
	@app.after_request
	def after_request(response):
				response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
				response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
				return response
	


	@app.route('/questions', methods=['GET'])
	def get_questions():
	'''
	  Handles GET request for getting all questions with pagination
	'''
		selection = Question.query.all();
		current_questions =paginate_questions(request , selection)
		categories = Category.query.all();

		# abort 404 if no questions
		if len(current_questions) == 0:
				 abort(404)
		try:
		 return jsonify({
						'success': True,
						'questions':  current_questions,
						'total_questions': len(selection),
						'categories':  {category.id: category.type for category in categories},
						'current_category': None
				})
		except:
			 abort(422)



	@app.route('/categories', methods=['GET'])
	def get_categories():
	'''
	   Handles GET request for getting all categories.
	'''
		try:
		 categories = Category.query.all();
		 return jsonify({
						'success': True,
						'categories':  {category.id: category.type for category in categories}	
				})
		except:
			abort(422)
	
	

	@app.route('/questions/<int:id>', methods=['DELETE'])
	def delete_question(id):
	'''
	   Handles DELETE requests for deleting a question by id.
	'''
		try:
				question= Question.query.get(id)

				 # abort 404 if no question found
				if question is None:
								abort(404)

				question.delete()

				return jsonify({
								'success': True,
								'deleted': id })
		except:
				abort(422)
	


	@app.route('/questions', methods=['POST'])
	def post_question():
		'''
        Handles POST requests for creating new questions and searching questions.
    '''
		body = request.get_json();
		search_term = body.get('searchTerm', None)
		if search_term :
				results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
				formatted_results = [result.format() for result in results]

				# abort 404 if there is no results
				if len(formatted_results) == 0:
				 	  abort(404)

				return jsonify({
				 'success': True,
				 'questions': formatted_results,
				 'total_questions': len(formatted_results)
				
				 })
		
		if search_term is None:
				 newQuestion = body.get('question')
				 newAnswer= body.get('answer')
				 newDifficulty = body.get('difficulty')
				 newCategory=  body.get('category')

				 if ((newQuestion is not None) and (newAnswer is not None) and (newDifficulty is not None) and (newCategory is not None)):
					 question = Question(question=newQuestion, answer=newAnswer , category=newCategory, difficulty=newDifficulty)
					 question.insert()
					 return jsonify({
										'success': True,
										'created': question.id,
										'question_created': question.question,
								})
				 else:
				 	# abort 422 if there is empty prameter
					 abort(422)
	


	@app.route('/categories/<int:id>/questions', methods=['GET'])
	def questions_by_category(id):
		'''
        Handles GET requests for getting questions based on category.
    '''
		 try:
				 category = Category.query.get(id);
				 questions = Question.query.filter(Question.category==id).all();
				 formatted_Questions = [Question.format() for Question in questions]
         
         # abort 404 if there is no category for the given id
				 if (category == None):
						abort(404)

				 return jsonify({
					'success': True,
					'questions': formatted_Questions,
					'totalQuestions': len(formatted_Questions),
					'currentCategory': category.type
						})
		 except:
				abort(422)
				 
	

	@app.route('/quizzes', methods=['POST'])
	def play():
		 '''
        Handles POST requests for playing quiz.
     '''
		try:
				body = request.get_json()
				
				previousQuestions =body.get('previous_questions', [ ])
			
				currentCategory_ID= body.get('quiz_category')['id']
        
        #if the user chose all Categories
				if currentCategory_ID not in ['1', '2', '3', '4', '5', '6']:
					totalQuestions =Question.query.all()
					questions = Question.query.filter(Question.id.notin_(previousQuestions)).all()
       
				else:
					totalQuestions =Question.query.filter(Question.category==currentCategory_ID).all()
					questions = Question.query.filter(Question.id.notin_(previousQuestions)).filter(Question.category==currentCategory_ID).all()

				formatted_Questions = [question.format() for question in questions]

				#display a new Question if there is more Questions in the choosen category
				if (len(previousQuestions) != len(totalQuestions)) :
				   nextQuestion= random.choice(formatted_Questions)
				else:
					nextQuestion = None

				if (nextQuestion is not None):
						return jsonify({
								'success': True,
								'question': nextQuestion
								})
				else:
					  return jsonify({
								'success': True
								})
		except:
			abort(422)
	
	

	 '''
        error handlers
   '''
	@app.errorhandler(422)
	def unprocessable(error):
				return jsonify({
						"success": False,
						"error": 422,
						"message": "Unprocessable: " 
				}), 422

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
				"success": False, 
				"error": 404,
				"message": "Not found"
				}), 404


	return app

		