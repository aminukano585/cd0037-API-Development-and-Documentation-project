from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    """
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1.0/categories', methods=['GET'])
    def read_all_categories():
        try:
            categories = Category.query.all()
            categories = {
                category.id: category.type for category in categories}

            return jsonify(
                {
                    'success': True,
                    'categories': categories
                }
            )

        except BaseException:
            abort(400)

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen
    for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1.0/questions', methods=['GET'])
    def read_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            categories = Category.query.all()
            categories = {
                category.id: category.type for category in categories}

            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all()),
                    'categories': categories,
                    'current_category': None
                }
            )

        except BaseException:
            abort(400)

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    'success': True,
                    'deleted': question_id,
                }
            )

        except BaseException:
            abort(422)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the
    end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/v1.0/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if 'searchTerm' in body:
            return search_questions(request, body['searchTerm'])

        try:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            for key in ['question', 'answer', 'difficulty', 'category']:
                if key not in body or body[key] is None or body[key] == '':
                    abort(422)

            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)
            question.insert()

            return jsonify(
                {
                    'success': True,
                    'created': question.format()
                }
            )

        except BaseException:
            abort(422)

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    def search_questions(request, search_term):
        try:
            selection = Question.query.filter(
                Question.question.ilike(
                    '%' + search_term + '%')).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection),
                    'current_category': None
                }
            )

        except BaseException:
            abort(400)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1.0/categories/<int:category_id>/questions',
               methods=['GET'])
    def read_questions_in_category(category_id):
        try:
            selection = Question.query.filter(
                Question.category == category_id).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection),
                    'current_category': category_id
                }
            )

        except BaseException:
            abort(404)

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def quiz_question():
        body = request.get_json()

        try:
            previous_questions = []
            if 'previous_questions' in body:
                previous_questions = body['previous_questions']

            if body['quiz_category']['id'] == 0:
                question = Question.query.filter(
                    Question.id.notin_(previous_questions)).order_by(
                    func.random()).first()
            else:
                question = Question.query.filter(
                    Question.category == body['quiz_category']['id'],
                    Question.id.notin_(previous_questions)).order_by(
                    func.random()).first()

            return jsonify({'success': True, 'question': question.format(
            ) if question is not None else None})

        except BaseException:
            abort(422)

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                'success': False,
                'error': 400,
                'message': 'Bad request'
            }
        ), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(
            {
                'success': False,
                'error': 404,
                'message': 'Not found'
            }
        ), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify(
            {
                'success': False,
                'error': 405,
                'message': 'Not allowed'
            }
        ), 405

    @app.errorhandler(422)
    def unprocessable_resource(error):
        return jsonify(
            {
                'success': False,
                'error': 422,
                'message': 'Unprocessable resource'
            }
        ), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify(
            {
                'success': False,
                'error': 500,
                'message': 'Server error'
            }
        ), 500

    return app
