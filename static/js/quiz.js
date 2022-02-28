const form = document.querySelector('#questions');
const url = 'http://127.0.0.1:5000/quiz';

async function callEndPoint(url, data) {
  try {
    const response = await axios({
      method: 'post',
      url: url,
      data: data,
    });
    return response.data;
  } catch (e) {
    console.log(`Unable to retrieve data from ${url}`);
  }
}

const getData = () => {
  const formData = new FormData(form);
  const data = {};

  for (let pair of formData.entries()) {
    data[pair[0].toString()] = pair[1];
  }
  return data;
};

function scrollTop() {
  window.scrollTo(0, 0);
}

function disableSubmitedQuestions(question) {
  for (let child of question.children) {
    child.firstElementChild.disabled = true;
  }
}

function checkAnswer(choice, correctChoice, isAnswerOk) {
  if (isAnswerOk) {
    choice.classList.add('text-success');
  } else {
    choice.classList.add('text-danger');
    correctChoice.classList.add('text-success');
  }
}

function showResult(avg) {
  const h3 = document.querySelector('#quiz-avg');

  h3.innerHTML = `${avg}% assertions`;
  if (avg < 50) {
    h3.innerHTML += ', keep trying';
    h3.style.color = 'red';
  } else {
    h3.innerHTML += ', well done!';
    h3.style.color = 'green';
  }
}

function checkQuestionsAfterSubmit(quizCheck) {
  quizCheck.forEach((quiz) => {
    const question = document.getElementById(quiz.question);
    const choiceId = quiz.choice;
    const choice = document.getElementById(choiceId);
    const isAnswerOk = quiz.is_correct;
    const correctChoiceId = quiz.correct_choice;
    const correctChoice = document.getElementById(correctChoiceId);

    disableSubmitedQuestions(question);
    checkAnswer(choice, correctChoice, isAnswerOk);
  });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = getData();
  const quizCheck = await callEndPoint(url, data);

  checkQuestionsAfterSubmit(quizCheck.results);
  showResult(quizCheck.avg);
  scrollTop();
});
