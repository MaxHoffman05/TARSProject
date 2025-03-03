/*
TARS Project - insert.js
Date: 2/24/2025 - 3/3/2025
Author: Max Hoffman
Purpose: Script to load the footer and nav bar HTML elements
*/

fetch("footer.html")
  .then((response) => response.text())
  .then((data) => {
    document.getElementById("footer").innerHTML = data;
  })
  .catch((error) => console.error("Error Loading Footer:", error));

fetch("nav.html")
  .then((response) => response.text())
  .then((data) => {
    document.getElementById("nav").innerHTML = data;
  })
  .catch((error) => console.error("Error Loading Navbar:", error));
