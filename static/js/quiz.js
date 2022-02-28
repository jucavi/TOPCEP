const form = document.querySelector('#questions');
const url = 'http://127.0.0.1:5000/quiz';

async function callEndPoint(url, data) {
  const response = await axios({
    method: 'post',
    url: url,
    data: data,
  });
  const results = await response.data.results;

  results.forEach((element) => {
    const question = document.getElementById(element.question);
    console.dir(question)
    const choiceId = element.choice;
    const choice = document.getElementById(choiceId);
    const isAnswerOk = element.is_correct;
    const correctChoiceId = element.correct_choice;
    const correctChoice = document.getElementById(correctChoiceId);

    for (let child of question.children) {
      child.firstElementChild.disabled = true;
    }

    if (isAnswerOk) {
      choice.classList.add('text-success');
    } else {
      choice.classList.add('text-danger');
      correctChoice.classList.add('text-success');
    }
  });
  window.scrollTo(0, 0);
}

const getData = () => {
  const formData = new FormData(form);
  const data = {};

  for (let pair of formData.entries()) {
    data[pair[0].toString()] = pair[1];
  }
  return data;
};

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const data = getData();
  callEndPoint(url, data);
});
