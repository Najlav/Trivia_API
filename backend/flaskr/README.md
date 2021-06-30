#Full Stack Trivia API Project

This project is a game in which players may test their knowledge by answering trivia questions. The project's objective was to build an API and test suite for implementing the following functionality:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

##Getting Started
###Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

###Backend
Once setup your virtual environment install the dependencies by running:
```
pip install requirements.txt
```
###frontend
NPM is used in the project to manage software dependencies install it by running:
```
npm install
```
###Running frontEnd
run the terminal:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
###running test
run the terminal:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
##API Reference
###Getting Started
-Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

-Authentication: This version of the application does not require authentication or API keys.
####Error Handling
Errors are returned as JSON in the following format:
```
{
	"success": False,
	"error": 422,
	"message": "Unprocessable: " 
}

{
	"success": False, 
	"error": 404,
	"message": "Not found"
}
```
The API will return two types of errors:
- 404 – resource not found
- 422 – unprocessable

###Endpoints
GET /questions
General:
- Returns a list of questions objects, categories , success value, and total number of questions
- Results are paginated in groups of 10. 
Sample: curl -X GET http://127.0.0.1:5000/questions
```
{
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "questions": [
          {
              "answer": "Colorado, New Mexico, Arizona, Utah", 
              "category": 3, 
              "difficulty": 3, 
              "id": 164, 
              "question": "Which four states make up the 4 Corners region of the US?"
          }, 
          {
              "answer": "Muhammad Ali", 
              "category": 4, 
              "difficulty": 1, 
              "id": 9, 
              "question": "What boxer's original name is Cassius Clay?"
          }, 
          {
              "answer": "Apollo 13", 
              "category": 5, 
              "difficulty": 4, 
              "id": 2, 
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          }, 
          {
              "answer": "Tom Cruise", 
              "category": 5, 
              "difficulty": 4, 
              "id": 4, 
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
          }, 
          {
              "answer": "Edward Scissorhands", 
              "category": 5, 
              "difficulty": 3, 
              "id": 6, 
              "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          }, 
          {
              "answer": "Brazil", 
              "category": 6, 
              "difficulty": 3, 
              "id": 10, 
              "question": "Which is the only team to play in every soccer World Cup tournament?"
          }, 
          {
              "answer": "Uruguay", 
              "category": 6, 
              "difficulty": 4, 
              "id": 11, 
              "question": "Which country won the first ever soccer World Cup in 1930?"
          }, 
          {
              "answer": "George Washington Carver", 
              "category": 4, 
              "difficulty": 2, 
              "id": 12, 
              "question": "Who invented Peanut Butter?"
          }, 
          {
              "answer": "Lake Victoria", 
              "category": 3, 
              "difficulty": 2, 
              "id": 13, 
              "question": "What is the largest lake in Africa?"
          }, 
          {
              "answer": "The Palace of Versailles", 
              "category": 3, 
              "difficulty": 3, 
              "id": 14, 
              "question": "In which royal palace would you find the Hall of Mirrors?"
          }
      ], 
      "success": true, 
      "total_questions": 19
  }
 ```
GET /categories
General:
- Returns a list of categories objects and success value
Sample: curl -X GET http://127.0.0.1:5000/categories
 ```
  {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
  }
 ```
DELETE /questions/<int:id>
General:
- Deletes a question by id using url parameters.
- Returns id of deleted question and success value.
Sample: curl -X DELETE http://127.0.0.1:5000/questions/2 

 ```
  {
      "deleted": 2, 
      "success": true
  }
 ```
POST /questions
General:
- search for questions using search term in parameters or creates a new question
- if search term is given, it returns a list of questions objects that has the search term,success value and the the number of total questions
- if a new question parameters were given, it returns the new question id, the question and success value

Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Who invented the electricity ?", "answer": "Benjamin Franklin", "difficulty": 3, "category": "4" }'
 ```
{
 	'success': True,
	'created': 24,
	'question_created': Who invented the electricity ?
}
 ```

Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "movie"}'
```
{
	"questions": [{
	          "answer": "Apollo 13", 
              "category": 5, 
              "difficulty": 4, 
              "id": 2, 
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996??"
	}],
 	 "success": true, 
     "total_questions": 1
}
 ```
GET /categories/<int:id>/questions
General:
- Gets questions by category id using url parameters.
- Returns JSON object with paginated matching questions.
Sample: curl http://127.0.0.1:5000/categories/1/questions
 ```
{
	'success': True,
	'questions': "questions": [
          {
              "answer": "The Liver", 
              "category": 1, 
              "difficulty": 4, 
              "id": 20, 
              "question": "What is the heaviest organ in the human body?"
          }, 
          {
              "answer": "Alexander Fleming", 
              "category": 1, 
              "difficulty": 3, 
              "id": 21, 
              "question": "Who discovered penicillin?"
          }, 
          {
              "answer": "Blood", 
              "category": 1, 
              "difficulty": 4, 
              "id": 22, 
              "question": "Hematology is a branch of medicine involving the study of what?"
          }
      ], ,
	'totalQuestions': 3,
	'currentCategory': "Science"
}
 ```
POST /quizzes
General:

- Allows users to play the quiz game.
- JSON request uses 2 parameters, category and previous questions.
- Returns JSON object with random question not among previous questions.

Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'
 ```
  {
      "question": {
          "answer": "Blood", 
          "category": 1, 
          "difficulty": 4, 
          "id": 22, 
          "question": "Hematology is a branch of medicine involving the study of what?"
      }, 
      "success": true
  }
 ```
##Authors
The API (__init__.py), test suite (test_flaskr.py), and this README were written by Najla Alshehri.
Udacity produced all additional project files, including the models and frontend, as a project template for the Full Stack Web Developer Nanodegree.


