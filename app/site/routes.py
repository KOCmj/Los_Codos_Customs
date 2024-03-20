from flask import Blueprint, render_template, session
from flask import flash, redirect, url_for, request, json

from flask_login import login_user, logout_user, LoginManager, current_user, login_required


site = Blueprint('site', __name__, template_folder = 'site_templates')



@site.route('/success')
def success():
    return render_template('success.html')


@site.route('/service')
def service():
    return render_template('service.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/join_lab')
def join_lab():
    return render_template('forms.html')

