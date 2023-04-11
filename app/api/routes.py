from flask import Blueprint, request, jsonify, render_template 
from helpers import token_required
from models import db, User, Whisky, whisky_schema, whiskys_schema 

api = Blueprint('api', __name__, url_prefix='/api') 

@api.route('/whiskys', methods = ['POST']) 
@token_required 
def create_whisky(current_user_token):
    name = request.json['name']
    country_origin = request.json['country_origin'] 
    type = request.json['type']
    abv = request.json['abv']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whisky = Whisky(name, country_origin, type, abv, user_token = user_token)

    db.session.add(whisky)
    db.session.commit() 

    response = whisky_schema.dump(whisky)
    return jsonify(response) 

@api.route('/whiskys', methods = ['GET'])
@token_required
def get_whisky(current_user_token):
    a_user = current_user_token.token
    whiskys = Whisky.query.filter_by(user_token = a_user).all()
    response = whiskys_schema.dump(whiskys)
    return jsonify(response)

@api.route('/whiskys/<id>', methods = ['GET'])
@token_required
def get_single_whisky(current_user_token, id): 
    whisky = Whisky.query.get(id)
    response = whisky_schema.dump(whisky)
    return jsonify(response)

@api.route('/whiskys/<id>', methods = ['POST', 'PUT']) 
@token_required
def update_whisky(current_user_token, id):
    whisky = Whisky.query.get(id)
    whisky.name = request.json['name']
    whisky.country_origin = request.json['country_origin']
    whisky.type = request.json['type']
    whisky.abv = request.json['abv']
    whisky.user_token = current_user_token.token

    db.session.commit()
    response = whisky_schema.dump(whisky)
    return jsonify(response)

@api.route('/whiskys/<id>', methods = ['DELETE'])
@token_required
def delete_whisky(current_user_token, id):
    whisky = Whisky.query.get(id)
    db.session.delete(whisky)
    db.session.commit()
    response = whisky_schema.dump(whisky)
    return jsonify(response)