/*
Script to load the footer

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
