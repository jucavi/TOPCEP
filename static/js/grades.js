const stringGrades = document.querySelector('#gradesList').value;
const grades = JSON.parse(stringGrades);

// 100% DIV
const sep = 1; // % bar separator
const numBars = grades.length;
console.log(numBars);
const barWidth = (100 - sep * numBars) / numBars;
console.log(barWidth);

const chart = document.querySelector('#bar-plot');
chart.style.position = 'relative';
let counter = 0;

for (let grade of grades) {
  const divBar = document.createElement('div');
  const divBarStyle = divBar.style;
  divBarStyle.width = `${barWidth}%`;
  divBarStyle.height = `${grade}%`;
  divBarStyle.position = 'absolute';
  divBarStyle.left = `${sep + (sep + barWidth) * counter}%`;
  divBarStyle.bottom = 0;
  divBarStyle.backgroundColor = '#706a53';
  divBar.innerText = grade
  divBar.classList.add('text-center')
  chart.append(divBar);
  counter++;
}
