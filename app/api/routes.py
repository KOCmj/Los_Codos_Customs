from flask import Blueprint, request, jsonify, render_template, flash
from helpers import token_required
from models import db, User, Car, cars_schema, car_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/cars', methods = ['POST'])
@token_required
def create_user(current_user_token):
    name = request.json['name']
    year = request.json['year']
    model = request.json['model']
    make = request.json['make']
    user_token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    car = Car(name, year, model, make, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_user(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_user(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_user(current_user_token, id):
    car = Car.query.get(id)
    car.name = request.json['name']
    car.year = request.json['year']
    car.model = request.json['model']
    car.make = request.json['make']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_user(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

