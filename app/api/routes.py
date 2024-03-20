from flask import Blueprint, request, jsonify, render_template, flash
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    city = request.json['city']
    state = request.json['state']
    street_address = request.json['address']
    zip_code = request.json['zip']
    postal_code = request.json['postal_code']
    region = request.json['region']
    user_token = current_user_token.token

    print(f'TEST: {current_user_token.token}')

    contact = Contact(name, email, city, first_name, last_name, street_address, state, zip_code, postal_code, region, user_token=user_token)

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

# Pulls one contact
@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)


# Update Contact/endpoint   
@api.route('/contacts/<id>', methods = ['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    contact = Contact.query.get(id)
    contact.name = request.json['name']
    contact.first_name = request.json['first_name']
    contact.last_name = request.json['last_name']
    contact.email = request.json['email']
    contact.city = request.json['city']
    contact.state = request.json['state']
    contact.street_address = request.json['address']
    contact.zip_code = request.json['zip']
    contact.postal_code = request.json['postal_code']
    contact.region = request.json['region']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

# Delete Contact/endpoint
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

