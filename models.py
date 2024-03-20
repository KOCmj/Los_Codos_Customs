from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets 

# Set variables for class instantiation 
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    street_address = db.Column(db.String(150), nullable = True, default = '')
    city = db.Column(db.String(150), nullable=True, default='')
    state = db.Column(db.String(150), nullable=True, default='')
    zip_code = db.Column(db.String(25), nullable=True, default='')
    region = db.Column(db.String(150), nullable=True, default='')
    postal_code = db.Column(db.String(25), nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, first_name='', last_name='', street_address='', city='', state='', zip_code='', region='', postal_code='', token = '',g_auth_verify=False):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.region = region
        self.postal_code = postal_code
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has successfully been added to the KOC database!'
    
class Contact(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(200))
    city = db.Column(db.String(150), nullable = False)
    state = db.Column(db.String(150), nullable = False)
    street_address = db.Column(db.String(150), nullable = False)
    zip_code = db.Column(db.String(20))
    postal_code = db.Column(db.String(20))
    region = db.Column(db.String(150), nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, email, city, first_name, last_name, street_address, state, zip_code, user_token, postal_code, region, id = ''):
        self.id = self.set_id()
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.city = city
        self.state = state
        self.street_address = street_address
        self.zip_code = zip_code
        self.postal_code = postal_code
        self.region = region

        self.user_token = user_token

    def __repr__(self):
        return f'The following contact has been added to the KOC club: {self.name}'
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
class ContactSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'first_name', 'last_name', 'email', 'city', 'state', 'street_address', 'zip_code', 'postal_code', 'region']

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many = True)
