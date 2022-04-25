from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # email is unique
        print(user)
        if user:
            # if check_password_hash(user.password, password):
            if user.password == password: # no hash version
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorect password, try again.', category='error')
        else:
            flash('Incorect password, try again.', category='error')    

    data = request.form
    print(data) # print data (test)
    return render_template("signIn.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        login=request.form.get('login')
        email=request.form.get('email')
        password=request.form.get('password')
        password2=request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 5:
            flash("E-mail must be greater than 5 characters.", category="error")
        elif len(login) < 2:
            flash("Login must be greater than 2 characters.", category="error")
        elif password != password2:
            flash("Entered passwords are not equal.", category="error")
        elif len(password) < 8:
            flash("Password must be greater than 8 characters", category="error")
        else:
            newUser = User(email=email, login=login, password=password)
            db.session.add(newUser) # dodanie użytkownika do bazy danych
            db.session.commit() # zapisanie zmian
            flash("Your account has been created!", category="success")
            data = request.form
            print(data)
            print(newUser.password)
            return redirect(url_for('views.home'))
    return render_template("signUp.html", user=current_user)
