const stringGrades = document.querySelector('#scoresList').value;
const grades = JSON.parse(stringGrades);

// 100% DIV
const sep = 1; // % bar separator
const numBars = grades.length;
const barWidth = (100 - sep * numBars) / numBars;

const chart = document.querySelector('#bar-plot');
chart.style.position = 'relative';
let counter = 0;

for (let grade of grades) {
  const divBar = document.createElement('div');
  const divBarStyle = divBar.style;
  const gradeText = document.createElement('div');

  gradeText.innerText = grade;
  gradeText.style.fontSize = '80%';
  gradeText.classList.add('grade');

  // style
  // gradeText.style.rotate = '-45deg'

  divBar.id = `bar${counter}`;
  divBar.classList.add('text-center');

  // style
  divBarStyle.width = `${barWidth}%`;
  divBarStyle.height = `${grade}%`;
  divBarStyle.position = 'absolute';
  divBarStyle.left = `${sep + (sep + barWidth) * counter}%`;
  divBarStyle.bottom = 0;
  divBarStyle.backgroundColor = grade > 50 ? '#99d98c' : '#ca6702';

  if (grade === 0) {
    divBarStyle.bottom = '1.4em';
  }

  divBar.append(gradeText);
  chart.append(divBar);
  counter++;
}
