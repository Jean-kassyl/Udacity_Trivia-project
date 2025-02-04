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

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## API REFERENCE 
---

### Getting Started

- Base URL: This app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000`.
- Authentication: This version does not require authentication or API Keys.

### Error Handling

Error are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "Bad request"
}

```
The API will return three errors types when requests fail:
- 400: Bad request
- 404: Not found
- 422: Unprocessable

### Endpoint

#### GET `/trivia/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
-sample: `curl "http://127.0.0.1:5000/trivia/categories"`

```
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}

```

#### GET `/trivia/questions?page=${integer}`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string
- Request arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, current category string and success, a boolean.
- sample: curl `http://127.0.0.1:5000/trivia/questions?page=1`

```
{
categories: {
1: "Science",
2: "Art",
3: "Geography",
4: "History",
5: "Entertainment",
6: "Sports"
},
current_category: "entertainment",
questions: [
{
answer: "Apollo 13",
category: 5,
difficulty: 4,
id: 2,
question: "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
},
{
answer: "Tom Cruise",
category: 5,
difficulty: 4,
id: 4,
question: "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
answer: "Maya Angelou",
category: 4,
difficulty: 2,
id: 5,
question: "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
{
answer: "Edward Scissorhands",
category: 5,
difficulty: 3,
id: 6,
question: "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
},
{
answer: "Muhammad Ali",
category: 4,
difficulty: 1,
id: 9,
question: "What boxer's original name is Cassius Clay?"
},
{
answer: "Brazil",
category: 6,
difficulty: 3,
id: 10,
question: "Which is the only team to play in every soccer World Cup tournament?"
},
{
answer: "Uruguay",
category: 6,
difficulty: 4,
id: 11,
question: "Which country won the first ever soccer World Cup in 1930?"
},
{
answer: "George Washington Carver",
category: 4,
difficulty: 2,
id: 12,
question: "Who invented Peanut Butter?"
},
{
answer: "Lake Victoria",
category: 3,
difficulty: 2,
id: 13,
question: "What is the largest lake in Africa?"
},
{
answer: "The Palace of Versailles",
category: 3,
difficulty: 3,
id: 14,
question: "In which royal palace would you find the Hall of Mirrors?"
}
],
success: true,
total_questions: 21
}

```
#### GET `/trivia/categories/${id}/questions`

- Fetches questions for a cateogry specified by id request argument.
- Request arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, current category string and success, a boolean to show that the operation succeed.
- sample: curl `http://127.0.0.1:5000/trivia/categories/1/questions`

```
{
categories: {
1: "Science",
2: "Art",
3: "Geography",
4: "History",
5: "Entertainment",
6: "Sports"
},
current_category: "Science"
questions: [
{
answer: "The Liver",
category: 1,
difficulty: 4,
id: 20,
question: "What is the heaviest organ in the human body?"
},
{
answer: "Alexander Fleming",
category: 1,
difficulty: 3,
id: 21,
question: "Who discovered penicillin?"
},
{
answer: "Blood",
category: 1,
difficulty: 4,
id: 22,
question: "Hematology is a branch of medicine involving the study of what?"
}
],
success: true,
total_questions: 21
}

```

#### POST `/trivia/questions`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```
- returns: An object with three keys, **success** to show that the operation succeeded, **created** which returns the id of the newly created question, and **total_questions**.
- sample: ` curl http://127.0.0.1:5000/trivia/questions -X POST -H "Content-Type: application/json" -d '{"question": "Heres a new question string","answer": "Heres a new answer string","difficulty": 1,"category": 3}'`

```
{
  "created": 27,
  "success": true,
  "total_questions": 22
}

```


#### DELETE `/trivia/questions/${id}`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- returns: An object with three keys, **success** to show that the operation succeeded, **deleted** which returns the id of the deleted question, and **total_questions**.
- sample: `curl -X DELETE http://127.0.0.1:5000/books/27`

```
{
  "deleted": 27,
  "success": true,
  "total_questions": 21
}

```

#### POST `/trivia/quizzes`

- Sends a post request in order to get a random question either within all the categories or per category
- Request Body:

```json
{
    "previous_questions": [1, 2, 21, 14],
    "quiz_category": {"type": "", "id": 0}
}
```
- Returns: a single new question object.
- sample: ` curl http://127.0.0.1:5000/trivia/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [],"quiz_category": {"type": "", "id": 0}}'`

```
{
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 17,
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}

- you might get a different question back as this endpoint send random question
```

#### POST `/trivia/questions/search`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term , the current category string and a boolean success.
- sample: ` curl http://127.0.0.1:5000/trivia/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`

```
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 21
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
