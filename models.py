from main import db
from flask import session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__='user'

    id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(64), default=None)
    # grades = db.Column(db.String(50), default=None)


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

    quizzes = db.relationship('Quiz', backref=db.backref('user'), lazy=True)

    def __repr__(self):
        return f'<User: {self.email}>'


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.String(32), primary_key=True)
    question = db.Column(db.Text(), nullable=False)
    answer = db.Column(db.String(32), default=None)

    def __repr__(self):
        return f'{self.question}'


class Choice(db.Model):
    __tablename__ = 'choice'

    id = db.Column(db.String(32), primary_key=True)
    choice = db.Column(db.String(), nullable=False)
    question_id = db.Column(db.String(32), db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', backref=db.backref('choices', lazy=True, cascade=('all', 'delete-orphan')))

    def __repr__(self):
        return f'{self.choice}'


class Quiz(db.Model):
    __tablename__='quiz'

    id = db.Column(db.String(32), primary_key=True)
    score = db.Column(db.Float(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)

    questions = db.relationship('Question', secondary='quizzesquestions', primaryjoin=('Question.id==QuizzesQuestions.question_id'))


    def __repr__(self):
        return f'{self.user} created at: {self.created_at}'


class QuizzesQuestions(db.Model):
    __tablename__= 'quizzesquestions'

    id = db.Column(db.String(32), primary_key=True)
    quizz_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.String(32), db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.String(32))


