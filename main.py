from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(env='develop'):
    from config import config

    app = Flask(__name__)
    app.config.from_object(config.get(env))

    db.init_app(app)

    with app.app_context():
        from models import User
        from auth import auth_bp
        from dashboard import dash_bp

        db.create_all()

        app.register_blueprint(auth_bp)
        app.register_blueprint(dash_bp)

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}

    return app