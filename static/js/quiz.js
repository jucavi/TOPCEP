const form = document.querySelector('#questions');
const questions = document.querySelectorAll('.question');
const url = `http://${window.location.host}/score`;
const submit = document.querySelector('#quiz-submit');
const quizTime = 10 * 60;
const startQuiz = document.querySelector('#start-quiz');
const startDiv = document.querySelector('#start');

function getTimeRemaining(endTime) {
  let seconds = Math.floor(endTime % 60);
  let minutes = Math.floor((endTime / 60) % 60);

  return [minutes, seconds];
}

function initClock() {
  let endTime = quizTime;

  const init = setInterval(() => {
    const [min, sec] = getTimeRemaining(endTime);

    startQuiz.innerText = `${min}m ${sec}s`;
    endTime--;

    if (endTime < 0) {
      clearInterval(init);

      startQuiz.classList.remove('start');
      startQuiz.classList.add('end');

      sendQuiz();
    }
  }, 1000);
}

// console.log(startQuiz)
startQuiz.addEventListener('click', (event) => {
  initClock();
});

// window.addEventListener('scroll', (event) => {
//   const lastKnownScrollPosition = this.scrollY;
//   if (lastKnownScrollPosition >= 104) {
//     startDiv.style.position = 'fixed'
//     startDiv.style.margin = 'auto'
//   } else {
//     startDiv.style.position = '';
//   }
//   console.log(lastKnownScrollPosition)
// })

async function callEndPoint(url, data) {
  try {
    axios.defaults.withCredentials = true;
    const response = await axios({
      method: 'POST',
      url: url,
      data: data,
      withCredentials: true,
    });
    return response.data;
  } catch (e) {
    console.log(e);
    console.log(`Unable to retrieve data from ${url}`);
  }
}

const getData = () => {
  const data = {};
  for (let question of questions) {
    const options = question.querySelectorAll('.option');
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

form.addEventListener('submit', (event) => {
  event.preventDefault();
  sendQuiz();
});

async function sendQuiz() {
  const data = getData();
  const quizCheck = await callEndPoint(url, data);

  checkQuestionsAfterSubmit(quizCheck.results);
  showResult(quizCheck.score);
  submit.disabled = true;
  scrollTop();
}
