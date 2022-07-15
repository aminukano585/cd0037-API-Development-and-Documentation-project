# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Endpoints Documentation

`GET '/api/v1.0/categories'`

- Request Arguments: None
- Returns: An object with two keys, `success` that signifies success of the request and `categories`, that contains an object of `id: category_string` key: value pairs.

```json
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

`GET '/api/v1.0/questions'`

- Request Arguments: None
- Returns: An object with five keys, `success` that signifies success of the request and `categories`, that contains an object of `id: category_string` key: value pairs. The `current_category` which should be null, the paginated list of `questions` in batches of 10, and the `total_questions`.

```json
{
  "categories": {
    "1": "Science", 
    ...
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}
```

`DELETE '/api/v1.0/questions/question_id'`

- Request Arguments: `question_id` of the question to be deleted
- Returns: An object with two keys, `success` that signifies success of the request and `deleted`, that contains the id of the deleted question.

```json
{
  "success": true,
  "deleted": 2
}
```

`POST '/api/v1.0/questions'`

- Request Arguments: parameters in the body of a request
- Returns: An object with two keys, `success` that signifies success of the request and `created`, that contains the created question.

```json
{
  "success": true,
  "created": {
    "answer": "Muhammad Ali", 
    "category": 4, 
    "difficulty": 1, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }
}
```

- If `search_term` is included in the body of the request, it returns result with the keys, `success` that signifies success of the request, the `questions` that satisfies the search, the number of `total_questions`, and the `current_category` which should be null.

```json
{ 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 4
}
```

`GET '/api/v1.0/categories/category_id/questions'`

- Request Arguments: None
- Returns: An object with four keys, `success` that signifies success of the request and the `current_category` of the questions, the paginated list of `questions` in batches of 10, and the `total_questions`.

```json
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 3
}
```

`POST '/api/v1.0/quizzes'`

- Request Arguments: parameters in the body of a request
- Returns: An object with two keys, `success` that signifies success of the request and `question`, that contains a random question. If `previous_question` is included in the request parameters, it will not be included.

```json
{
  "success": true,
  "question": {
    "answer": "Muhammad Ali", 
    "category": 4, 
    "difficulty": 1, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
