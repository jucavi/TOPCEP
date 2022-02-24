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


    def is_authenticated(self):
        session_token = session.get('token')
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
        return f'< User >: {self.email}'