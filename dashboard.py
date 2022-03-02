from ast import keyword
from flask import Blueprint, render_template, make_response, request
from auth import current_user, login_required, User
from main import db
from random import shuffle
from models import Question
from flask_cors import CORS


dash_bp = Blueprint('dashboard', __name__)
CORS(dash_bp, supports_credentials=True)

@dash_bp.route('/')
def index():
    return render_template('index.html', user=current_user())


@dash_bp.route('/workspace')
@login_required
def workspace():
    return render_template('workspace.html', title='workspace', user=current_user())


@dash_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = Question.query.all()
    shuffle(questions)
    res = make_response(render_template('quiz.html', title='Quiz', user=current_user(), questions=questions))
    res.set_cookie('id', current_user().id)
    return res


@dash_bp.route('/score', methods=['POST'])
def score():
    result = {'results': [], 'avg': 0}
    count = 0
    form = request.get_json()
    total = 16
    cookies = request.cookies
    _current_user = User.query.get(cookies['id'])

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

    avg = round(count / total * 100 , 2)
    result['avg'] = avg

    grades = append_grade(_current_user.grades, avg)
    _current_user.grades = grades
    db.session.add(_current_user)
    db.session.commit()

    return result


@dash_bp.route('/grades')
@login_required
def grades():
    user = current_user()
    grades = user.grades or 'Make some Quizzes'
    return render_template('grades.html', title='Grades', grades=parse_grades(grades), user=user)


def append_grade(grades, avg):
    grades = parse_grades(grades)
    grades.append(avg)

    return str(grades)


def parse_grades(grades):
    if grades:
        return [float(grade) for grade in grades[1:-1].split(', ')]
    return []