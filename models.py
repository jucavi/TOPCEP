from main import db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(64), default=None)
    grades = db.Column(db.String(50), default=None)


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def is_authenticated(self, token=None):
        session_token = session.get('token') or token
        return session_token and (self.token == session_token)

    def reset_token(self):
        self.token = None

    @property
    def username(self):
        try:
            return self.email.split('@')[0].capitalize()
        except Exception:
            return 'Anonymous'


    def __repr__(self):
        return f'<User: {self.email}>'


class Question(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    question = db.Column(db.Text(), nullable=False)
    answer = db.Column(db.String(32), default=None)

    def __repr__(self):
        return f'{self.question}'


class Choice(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    choice = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.String(32), db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', backref=db.backref('choices', lazy=True, cascade=('all', 'delete-orphan')))

    def __repr__(self):
        return f'{self.choice}'