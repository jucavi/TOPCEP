const form = document.querySelector('#questions');

const callEndPoint = async url => {
  result = await axios.post(url);
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  console.dir(event)
});