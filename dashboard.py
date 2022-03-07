from configparser import SectionProxy
from flask import Blueprint, render_template, make_response, request, g
from auth import current_user, login_required
from main import db
from random import shuffle
from uuid import uuid4
from models import Question, Quiz, QuizzesQuestions, Choice
# from flask_cors import CORS


dash_bp = Blueprint('dashboard', __name__)
# CORS(dash_bp, supports_credentials=True)

@dash_bp.route('/')
def index():
    return render_template('index.html', user=current_user())


@dash_bp.route('/workspace')
@login_required
def workspace():
    return render_template('workspace.html', title='workspace', user=current_user())


QUIZ_QUESTIONS = 10
@dash_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    questions = Question.query.all()
    shuffle(questions)
    res = make_response(render_template('quiz.html', title='Quiz', user=current_user(), questions=questions[:QUIZ_QUESTIONS]))
    res.set_cookie('id', current_user().id, secure=True)
    return res


@dash_bp.route('/score', methods=['POST'])
def score():
    result = {'results': [], 'avg': 0}
    count = 0
    form = request.get_json()
    cookies = request.cookies
    print(form)
    print(cookies)

    # quiz = Quiz(id=uuid4().hex, user_id=cookies['id'])

    # for question_id, choice_id in form.items():
    #     question = Question.query.get(question_id)
    #     is_correct = question.answer == choice_id
    #     result['results'].append({
    #             'question': question_id,
    #             'choice': choice_id,
    #             'correct_choice': question.answer,
    #             'is_correct': is_correct
    #     })
    #     if is_correct:
    #         count += 1

    #     qq = QuizzesQuestions(id=uuid4().hex, quizz_id=quiz.id, question_id=question_id, answer=choice_id)
    #     db.session.add(qq)


    # score = round(count / QUIZ_QUESTIONS * 100)
    # result['score'] = score

    # quiz.score = score
    # db.session.add(quiz)
    # db.session.commit()

    return result


@dash_bp.route('/grades')
@login_required
def scores():
    user = current_user()
    scores = get_scores(user) or 'Make some Quizzes'
    return render_template('scores.html', title='Grades', scores=scores, user=user)


@dash_bp.app_template_filter('shuffle')
def make_shuffle(iter):
    shuffle(iter)
    return iter


def get_scores(user):
    quizzes = user.quizzes
    print(user, quizzes)
    if not quizzes:
        return None
    return [quiz.score for quiz in quizzes]
