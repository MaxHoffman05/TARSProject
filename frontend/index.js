/*
TARS Project
Date: 2/24/2025 - 3/3/2025
Author: Max Hoffman
Purpose: Handles the front end logic for the TARS website
*/

import { BACKEND_URL } from "./config.js";
import SpeechBubble from "./speechBubble.js";

//Buttons
const submitButton = document.getElementById("submitTars");
const deleteButton = document.getElementById("deleteHistory");
const historyButton = document.getElementById("viewHistory");
submitButton.addEventListener("click", sendQuestion);
deleteButton.addEventListener("click", deleteHistory);
historyButton.addEventListener("click", viewHistory);

const textField = document.getElementById("inputTars");
const responseWindow = document.getElementById("tarsResponseWindow");
const humorGroup = document.querySelectorAll('input[name="humor"]');
const histModal = document.getElementById("historyModal");

//Constants
//Max number of characters to display from the user only
//TARS has no variable limit but in his prompt he is told to keep responses under 100 characters unless otherwise instructed
const MAX_TEXT_DISPLAY = 50;

//gets the humor setting from the radio buttons
function getHumorSetting() {
  for (const element of humorGroup) {
    if (element.checked) {
      console.log(element.value);
      return element.value;
    }
  }
  //should never get here, but just in case something is changed in the HTML side default will always be returned
  return "def";
}

//submits user question on enter
document.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    sendQuestion();
  }
});

//Method to send question to groq
function sendQuestion() {
  var userQuestion = textField.value;
  textField.value = "";

  //check to see if the text field is empty
  if (userQuestion.trim() != "") {
    console.log("Sending question: " + userQuestion);
    //disable buttons and input field
    textField.disabled = true;
    historyButton.disabled = true;
    deleteButton.disabled = true;

    var humorSetting = getHumorSetting();
    //send user question to response window
    editResponseWindow(userQuestion, true);
    //send question and humor setting to backend

    fetch(BACKEND_URL + "/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userQuestion, humor: humorSetting }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Result: " + data);
        //send tars response to response window
        const tarsResponse = JSON.stringify(data);
        editResponseWindow(tarsResponse, false);
        //renable buttons and input field
        textField.disabled = false;
        historyButton.disabled = false;
        deleteButton.disabled = false;
        textField.focus();
      })
      .catch((error) => console.error("Error : " + error));
  } else {
    console.log("Text field is empty");

    textField.value = "";
  }
}

//method deletes chat_history variable stored in redis by sending a delete request to the backend, also clears response window on the frontend side
function deleteHistory() {
  fetch(BACKEND_URL + "/del", {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.error("Error : " + error));

  responseWindow.innerHTML = "";
}

//Method for displaying Speech bubbles from the speechBubble.js class
//This will create the speech bubble for TARS and the user, and add it to the response window
function editResponseWindow(text, user) {
  var newSpeechBubble;
  if (user) {
    //create speech bubble element for user
    newSpeechBubble = new SpeechBubble(text, true);
    //modify text if neccessary
    if (text.length > MAX_TEXT_DISPLAY) {
      console.log("Text too long");
      newSpeechBubble.element.textContent =
        text.substring(0, MAX_TEXT_DISPLAY) + "...";
    }
  } else {
    //create speech bubble element for tars
    text = text.substring(1, text.length - 1);
    newSpeechBubble = new SpeechBubble(text, false);
  }
  newSpeechBubble.element.textContent = text;
  //add new speech bubble to the response window, and add scroll height
  responseWindow.appendChild(newSpeechBubble.element);
  // Ensure that response window can scroll
  responseWindow.style.overflowY = "auto";
  responseWindow.style.height = responseWindow.scrollHeight + "px";
}

//method that gets chat history from backend and shows modal with data populated from /history
function viewHistory() {
  var body = document.getElementById("modalDynamic");
  //Get Request to the backend for the history JSON
  fetch(BACKEND_URL + "/history", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Recieved history: " + data);
      //insert data into modal
      //Convert to string
      const list = JSON.stringify(data);
      //pass to function and convert to html list
      const table = parseJSON(list);

      //clear text so there arent duplicates
      body.textContent = "";
      //add to modal
      body.appendChild(table);
      console.log(list);
    })
    .catch((error) => console.error("Error Fetching History : " + error));
  //create modal with body from get request to backend
  var newModal = new bootstrap.Modal(histModal);
  //show the modal
  newModal.show();
}

//dynamically creates Bootstrap table based on JSON data from backend from the /history route for Bootstrap modal
function parseJSON(jsonList) {
  const data = JSON.parse(jsonList);

  //create bootstrap table
  var table = document.createElement("table");
  table.className = "table table-bordered table-striped";

  //create thead and tr
  var headerRow = document.createElement("thead");
  headerRow.className = "thead-dark";
  var tr = document.createElement("tr");
  //setup header row with headings
  var headerCell1 = document.createElement("th");
  var headerCell2 = document.createElement("th");
  headerCell1.scope = "col";
  headerCell2.scope = "col";
  headerCell1.innerHTML = "Question";
  headerCell2.innerHTML = "Response";
  //add them to the table
  tr.appendChild(headerCell1);
  tr.appendChild(headerCell2);
  headerRow.appendChild(tr);
  table.appendChild(headerRow);

  //setup rows of data
  //for each question and response in data we add it to the body
  var body = document.createElement("tbody");
  for (var i = 0; i < data.length - 1; i += 2) {
    var row = document.createElement("tr");
    var cell1 = document.createElement("td");
    var cell2 = document.createElement("td");
    cell1.textContent = data[i] || "";
    cell2.textContent = data[i + 1] || "";

    row.appendChild(cell1);
    row.appendChild(cell2);
    console.log("adding row" + data[i + 1]);
    //append each row to the body
    body.appendChild(row);
  }

  table.appendChild(body);
  return table;
}
