from flask import Blueprint
from flask.templating import render_template
from flask_login import login_required, current_user

from website.models import User


views=Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/animals')
def animals():
    return render_template("animals.html", user=current_user)