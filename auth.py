from nis import cat
from textwrap import wrap
from flask import Blueprint, redirect, request, render_template, flash, session, url_for
from models import User
from uuid import uuid4
import secrets
from main import db
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email and password:
            try:
                user = User(id=uuid4().hex, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()

                flash('User successfully created.', category='success')
                return redirect(url_for('auth.login'))

            except Exception:
                flash('Email already in use', category='warning')

    return render_template('signup.html', submit='signup', title='Sign up')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                token = secrets.token_hex()
                user.token = token

                session['id'] = user.id
                session['token'] = token

                db.session.add(user)
                db.session.commit()
                return redirect(url_for('dashboard.workspace'))

            else:
                flash('Invalid password', category='danger')
        else:
            flash('User not found.', category='danger')

    return render_template('login.html', submit='login', title='Log in')

@auth_bp.route('/logout')
def logout():
    _id = session.get('id')
    user = User.query.get(_id)
    if user:
        user.reset_token()
        db.session.add(user)
        db.session.commit()
    session.pop('id', None)
    session.pop('token', None)

    return redirect(url_for('dashboard.index'))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _id = session.get('id')
        if _id:
            user = User.query.get(_id)
            try:
                if user.is_authenticated():
                    return func(*args, **kwargs)
            except Exception:
                pass
            
        flash('You must be log in to access this page', category='warning')
        return redirect(url_for('auth.login'))
    return wrapper
