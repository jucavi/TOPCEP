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
# @login_required
def quiz():
    if request.method == 'POST':
        result = {'results': []}
        count = 0
        total = 0
        form = request.get_json() or request.form
        for question_id, choice_id in form.items():
            question = Question.query.get(question_id)
            is_correct = question.answer == choice_id
            result['results'].append({
                    'question': question_id,
                    'choice': choice_id,
                    'correct_choice': question.answer,
                    'is_correct': is_correct
            })
            if is_correct:
                count += 1
            total += 1

        avg = round(count / total * 100 , 2)
        return result

    questions = Question.query.all()
    return render_template('quiz.html', title='Quiz', user=g.user, questions=questions)