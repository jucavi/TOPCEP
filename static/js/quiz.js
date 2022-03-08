const form = document.querySelector('#questions');
const questions = document.querySelectorAll('.question');
const url = 'http://localhost:5000/score';
const submit = document.querySelector('#quiz-submit');

async function callEndPoint(url, data) {
  try {
    axios.defaults.withCredentials = true;
    const response = await axios({
      method: 'POST',
      url: url,
      data: data,
      withCredentials: true
    });
    return response.data;
  } catch (e) {
    console.log(e)
    console.log(`Unable to retrieve data from ${url}`);
  }
}

const getData = () => {
  const data = {};
  for (let question of questions) {
    const options = question.querySelectorAll('.option')
    for (let option of options) {
      if (option.checked) data[option.name] = option.value;
    }
    if (!data[question.id]) data[question.id] = null;
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
    if (choice) {
      choice.classList.add('text-danger');
      correctChoice.classList.add('text-success');
    }
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
  showResult(quizCheck.score);
  submit.disabled = true;
  scrollTop();
});
