document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("registerBtn").addEventListener("click", function() {
      document.getElementById("popup").style.display = "block";
    });

    document.getElementsByClassName("close")[0].addEventListener("click", function() {
      document.getElementById("popup").style.display = "none";
    });

    document.getElementById("registrationForm").addEventListener("submit", function(event) {
      event.preventDefault(); 

    });
  });