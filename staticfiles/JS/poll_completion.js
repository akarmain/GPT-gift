document.querySelector("#display").querySelectorAll(".question_div").forEach((e) =>{
      question_id = e.querySelector("#question_id").value
      if (e.querySelector("#answer_type_input").value == "plural"){
        e.querySelectorAll(".answer_div").forEach((event) =>{
          var checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkbox.value = event.querySelector("#answer_id").value
          checkbox.setAttribute("name", question_id);
          event.prepend(checkbox)
        })
      }
      if (e.querySelector("#answer_type_input").value == "singular"){
        e.querySelectorAll(".answer_div").forEach((event) =>{
          var radio = document.createElement("input");
          radio.type = "radio";
          radio.id = "radio_input"
          radio.value = event.querySelector("#answer_id").value
          radio.setAttribute("name", question_id);
          event.prepend(radio);
          var radio = document.createElement("input");

        })
      }
      if (e.querySelector("#answer_type_input").value == "detailed"){
        var answer_div = document.createElement("div");
        answer_div.classList.add("answer_div");
        var answer_input = document.createElement("input");
//        console.log(e.querySelector("#answer_id"))
        answer_input.name = "D" + e.querySelector("#answer_id").value
        answer_div.append(answer_input)
        e.append(answer_div)
      }
})

