/*
TARS Project
Date: 2/26/2025 -
Author: Max Hoffman
Purpose: SpeechBubble class for response window, used by TARS and User
*/

const backgroundprimary = "#4a5057";

class SpeechBubble {
  constructor(text, user) {
    this.text = text;
    this.element = document.createElement("div");
    this.element.className = "question";
    this.element.classList.add("animate");

    this.element.style.padding = ".5rem";
    this.element.style.width = "fit-content";
    this.element.style.backgroundColor = backgroundprimary;
    this.element.style.fontSize = "1rem";
    this.element.style.borderRadius = "1rem";
    this.element.style.marginTop = "1rem";
    this.element.style.marginBottom = "1rem";
    this.element.style.display = "inline-block"; // Changed from block to inline-block for flex
    this.element.style.maxWidth = "80%"; // Prevent overflow

    // Conditional styling for user or TARS messages
    if (user) {
      this.element.style.alignSelf = "flex-end"; // Align user message to the right
    } else {
      this.element.style.alignSelf = "flex-start"; // Align TARS message to the left
    }
  }
}

export default SpeechBubble;
