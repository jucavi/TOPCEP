from os import path
import json
from uuid import uuid4
from models import Question, Choice
from main import create_app, db

app = create_app()
basedir = path.abspath(path.dirname(__file__))
filepath = path.join(basedir, 'pcep.json')

if not path.exists(filepath):
    print('File not found.')
    exit(1)

with open(filepath) as f:
    question_blocks = json.load(f)

# Only for local work comment it later
# if question_blocks:
#     question_blocks = {
#         "2_Control_Flow_Conditional_Blocks_and_Loops": question_blocks["2_Control_Flow_Conditional_Blocks_and_Loops"]
#     }

with app.app_context():
    for block, quizzes in question_blocks.items():
        for quiz in quizzes:
            try:
                question = Question(id=uuid4().hex, question=quiz['question'])
                for i, choice in enumerate(quiz['options']):
                    c = Choice(id=uuid4().hex, choice=choice, question=question)
                    if quiz['answer'] == i:
                        question.answer = c.id
                    question.choices.append(c)
                db.session.add(question)
            except Exception as e:
                print(e)

    db.session.commit()