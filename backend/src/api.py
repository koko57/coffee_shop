import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8100"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials',
                         'true')

    return response


'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })


'''
TODO implement endpoint
        it should require the 'get:drinks-detail' permission
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
def get_drinks_detail():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })


'''
TODO implement endpoint
    POST /drinks
        it should require the 'post:drinks' permission
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
def add_new_drink():
    body = request.get_json()
    title = body.get('title', None)
    recipe = str(json.dumps(body.get('recipe', None)))
    drink = Drink(title=title, recipe=recipe)
    try:
        drink.insert()
    except:
        abort(500)

    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


'''
TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should require the 'patch:drinks' permission
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def edit_drink(drink_id):
    drink = Drink.query.filter_by(id=drink_id).first()
    body = request.get_json()
    title = body.get('title', None)
    recipe = str(json.dumps(body.get('recipe', None)))
    drink.title = title
    drink.recipe = recipe

    try:
        drink.update()
    except:
        abort(500)

    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


'''
TODO implement endpoint
    DELETE /drinks/<id>
        it should respond with a 404 error if <id> is not found
        it should require the 'delete:drinks' permission
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = Drink.query.filter_by(id=drink_id).first()
    id = drink.long()['id']
    try:
        drink.delete()
    except:
        abort(500)

    return jsonify({
        "success": True,
        "drinks": id
    })


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500


'''
TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
