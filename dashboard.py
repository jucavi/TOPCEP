from flask import Blueprint, render_template
from auth import login_required, g, request
from main import db
from models import Question

dash_bp = Blueprint('dashboard', __name__)


@dash_bp.route('/')
def index():
    return render_template('index.html', user=g.user)


@dash_bp.route('/workspace')
@login_required
def workspace():
    return render_template('workspace.html', title='workspace', user=g.user)


@dash_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = Question.query.all()

    if request.method == 'POST':
        form = request.form
        result = {'results': []}
        for question_id, choice_id in form.items():
            question = Question.query.get(question_id)
            result['results'].append({
                    'question': question_id,
                    'answer': choice_id,
                    'correct_answer': question.answer,
                    'correct': question.answer == choice_id
                })
            return result

    return render_template('quiz.html', title='Quiz', user=g.user, questions=questions)