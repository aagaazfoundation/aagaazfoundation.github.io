/* Aagaaz Foundation. No tracking, no cookies, no storage. Two small jobs only. */
(function () {
  "use strict";

  /* 1. AGE CHOICE on "What to do first"
     Without this script both sets of notes show, each clearly labelled.
     The choice is kept only while the page is open. Nothing is saved. */
  var choice = document.querySelector("[data-age-choice]");
  if (choice) {
    choice.hidden = false;
    var scope = document.getElementById("main");
    var buttons = choice.querySelectorAll("button[data-age]");
    Array.prototype.forEach.call(buttons, function (button) {
      button.addEventListener("click", function () {
        var age = button.getAttribute("data-age");
        if (age === "both") { scope.removeAttribute("data-show-age"); }
        else { scope.setAttribute("data-show-age", age); }
        Array.prototype.forEach.call(buttons, function (b) {
          b.setAttribute("aria-pressed", b === button ? "true" : "false");
        });
      });
    });
  }

  /* 2. Close the help sheet or the menu when someone taps outside it. */
  document.addEventListener("click", function (event) {
    var open = document.querySelectorAll(".helpbar__help[open], .menu[open]");
    Array.prototype.forEach.call(open, function (d) {
      if (!d.contains(event.target)) { d.removeAttribute("open"); }
    });
  });
})();
