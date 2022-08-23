import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, question):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return question[start:end]


def define_current_category(query):
    current_category = {}
    if len(query) == 0:
            abort(404)

    else:
        for quest in query:
            q = Category.query.all()
            for cat in q:
                if quest['category'] == cat.id:
                    current_category[cat.id] = cat.type

        
    return current_category

def define_categories():
        q = Category.query.all()
        categories = {}
        for cat in q:
            categories[cat.id] = cat.type

        return categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/trivia/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorize, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS' )
        return response
        
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

   
    @app.route('/trivia/categories')
    def get_categories():
        # categories = Category.query.order_by(Category.id).all()
        # show_categories = [category.format() for category in categories]
        # print(categories)
        return jsonify({
            "success": True,
            "categories": define_categories(),
            "all_categories": len(Category.query.all())
        })




        


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/trivia/questions')
    def get_questions():
        bod = {}
       
        questions = Question.query.order_by(Question.id).all()
        #current_category = []
        formatted_questions = [question.format() for question in questions]
        paginated_questions = paginate_questions(request, formatted_questions)
        # if len(paginated_questions) == 0:
        #     abort(404)

        # else:
        #     for quest in paginated_questions:
        #         q = Category.query.all()
        #         for cat in q:
        #             if quest['category'] == cat.id:
        #                 current_category.append(cat.type)

        #     categories = set(current_category)
        
            
        bod["success"] = True
        bod['questions'] = paginated_questions
        bod['total_questions'] = len(Question.query.all())
        bod['current_category'] = define_current_category(paginated_questions)
        bod['categories'] = define_categories()
       
        

        return jsonify(bod)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/trivia/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        print(question_id)
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is not None:
            question.delete()
        else:
            abort(422)
        return jsonify({
            "success": True,
            "deleted": question_id,
            "total_questions": len(Question.query.all())

        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/trivia/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        print(body)
        id = ""
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        item = Question(question=new_question, answer=new_answer,difficulty=new_difficulty, category=new_category)
        if (item.question == None) and (item.answer == None) and (item.category == None) and (item.difficulty == None):
            abort(422)
        else: 
            item.insert()
            id = item.id

        return jsonify({
            "success": True,
            "created": id,
            "total_questions": len(Question.query.all())

        })
        
        
        
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/trivia/questions/search', methods=['POST'])
    def search_questions():
        search = request.get_json()['searchTerm']
        res = []
        if search == "":
            return jsonify({
                "success": True,
                "questions": res,
                "total_questions": len(Question.query.all()),
                "current_category": res
            })
        q = Question.query.filter(Question.question.ilike(f'%{search}%'))
        formated_questions = [question.format() for question in q]
        paginated_questions= paginate_questions(request, formated_questions)

        return jsonify({
                "success": True,
                "questions": paginated_questions,
                "total_questions": len(Question.query.all()),
                "current_category": define_current_category(paginated_questions)
            })
         
        
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/trivia/categories/<int:category_id>/questions', methods=["GET"])
    def get_questions_basedOn_category(category_id):
        q = Question.query.filter(Question.category == str(category_id)).all()
        formated_questions = [question.format() for question in q]
        paginated_questions = paginate_questions(request, formated_questions)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(Question.query.all()),
            "current_category": define_current_category(paginated_questions)
        })


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/trivia/quizzes', methods=['POST'])
    def get_question_toPlay_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')

        print(previous_questions)
        

        random_question = ""

        if quiz_category is None or (quiz_category['id'] == 0):
            q = Question.query.all()
            questions = []
            for quest in q:
                if quest.id not in previous_questions:
                    questions.append(quest)
   
            randNumber = random.randrange(0, len(questions))
            random_question = questions[randNumber]
            
        else:
            q = Question.query.filter(Question.category == str(quiz_category['id'])).all()
            questions = []
            for quest in q:
                if quest.id not in previous_questions:
                    questions.append(quest)
  
            randNumber = random.randrange(0, len(questions))
            random_question = questions[randNumber]
            

        return jsonify({
            "success": True,
            "question": random_question.format()    
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(404)
    def not_found(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"     
        })
    
    return app

