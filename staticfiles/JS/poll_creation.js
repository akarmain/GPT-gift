const answer_type_div = document.createElement('select');
answer_type_div.setAttribute('class', 'answer_type');
answer_type_div.setAttribute('name', 'answer_type');

const option1 = document.createElement('option');
option1.textContent = 'Одиночный выбор';
answer_type_div.appendChild(option1);

const option2 = document.createElement('option');
option2.textContent = 'Множественный выбор';
answer_type_div.appendChild(option2);

const option3 = document.createElement('option');
option3.textContent = 'Открытый вопрос';
answer_type_div.appendChild(option3);


empty_div = document.createElement('div');


document.querySelector("#display").append(empty_div)
document.querySelector("#display").append(empty_div.cloneNode(true))

const link_slug = document.location.origin + "/polls/" + document.querySelector("#poll_link_slug").value;

document.querySelector("#copy_link_btn").onclick = function () {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(link_slug)
      .then(() => {
        console.log('Link copied successfully');
      })
      .catch((error) => {
        console.error('Error copying link:', error);
      });
  } else {
    console.error('Clipboard API not supported',  document.querySelector("#poll_link_slug").value);
  }
}

answer_check = false;


document.querySelector("#display").querySelectorAll(".new_question").forEach((e) => {


  var answer_type_div_clone = answer_type_div.cloneNode(true);

  var add_answer = document.createElement('div');
  add_answer.textContent = "Добавить ответ";
  add_answer.setAttribute("class", "add_answer");
  add_answer.setAttribute("class", "btn btn-primary")

  e.appendChild(answer_type_div_clone);

  if (e.querySelector("#answer_type_input").value == "plural")
    e.querySelector(".answer_type").options[1].selected = true;
  if (e.querySelector("#answer_type_input").value == "detailed")
    e.querySelector(".answer_type").options[2].selected = true;


  var answer_div = document.createElement('div');
  e.appendChild(answer_div);

  e.appendChild(add_answer);
  var answer_input = document.createElement('input');
  answer_input.classList.add("answer_input");
  answer_input.setAttribute("class", "form-control")
  answer_input.setAttribute("disabled", "disabled")
  answer_input.setAttribute("placeholder", "Закрытое поле ввода")


  answer_type_div_clone.oninput = function () {
    if (this.value == this[2].value) {
      add_answer.style.display = "none";
      answer_div.replaceChildren();
      answer_input.setAttribute("readonly", "true")
      answer_div.append(answer_input);
    } else {
      add_answer.style.display = "";
      answer_input.remove();
    }

  }


  add_answer.onclick = function () {
    var answer_input = document.createElement('input');
    answer_input.setAttribute("class", "answer_input form-control");
    answer_input.setAttribute("name", "new_question");
    answer_input.setAttribute("name", "");

    answer_div.append(answer_input);
  }
})


document.querySelector("#add_question_button").onclick = function (event) {
  event.preventDefault();


  var question_div = document.createElement('div');
  question_div.classList.add("new_question")
  var hr = document.createElement('hr');
  var question_input = document.createElement('input');
  var answer_type_div_clone = answer_type_div.cloneNode(true);
  question_div.appendChild(document.createElement('br'));
  question_div.appendChild(question_input);
  question_div.appendChild(answer_type_div_clone);
  question_div.appendChild(document.createElement('br'));


  var add_answer = document.createElement('div');
  add_answer.textContent = "Добавить ответ";
  add_answer.setAttribute("class", "add_answer btn btn-primary");
  question_input.setAttribute("class", "question_title")
  question_input.setAttribute("placeholder", "Текст вопроса")


  var answer_div = document.createElement('div');
  question_div.appendChild(answer_div);

  question_div.appendChild(add_answer);
  var answer_input = document.createElement('input');

  answer_type_div_clone.oninput = function () {
    if (this.value == this[2].value) {
      add_answer.style.display = "none";
      answer_div.replaceChildren();
      answer_input.setAttribute("readonly", "true")
      answer_input.setAttribute("class", "answer_input");
      answer_div.append(answer_input);
    } else {
      add_answer.style.display = "";
      answer_input.remove();
    }

  }
  document.querySelector("#display").appendChild(question_div, this);

  add_answer.onclick = function () {
    var answer_input = document.createElement('input');
    answer_input.setAttribute("class", "answer_input form-control");
    answer_input.setAttribute("name", "new_question");
    answer_div.append(answer_input);
  }


  question_div.appendChild(hr.cloneNode(true));


}

document.querySelector("#send").onclick = function () {
  DATA = []
  document.querySelector("#display").querySelectorAll(".new_question").forEach((e) => {
    dict = {}
    dict["title"] = e.querySelector(".question_title").value;
    dict["type"] = e.querySelector(".answer_type").value;

    answers = []
    e.querySelectorAll(".answer_input").forEach((event) => {
      answers.push(event.value);
    })
    dict["answers"] = answers;

    DATA.push(dict);
  });

  DATA = JSON.stringify(DATA);
  document.getElementById('DATA').value = DATA;
}
