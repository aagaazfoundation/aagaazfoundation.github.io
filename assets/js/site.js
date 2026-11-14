/* Aagaaz Foundation. No tracking, no cookies, no storage. Three small jobs only. */
(function () {
  "use strict";

  /* 1. QUICK EXIT
     Hides the page at once (so nothing lingers on a slow connection), then
     replaces this page with a neutral one so the Back button does not return here.
     Works as a plain link if this script has not loaded. Esc pressed twice does the same. */
  var exitLink = document.querySelector("[data-quick-exit]");
  function quickExit(event) {
    if (event) { event.preventDefault(); }
    var url = exitLink ? exitLink.href : "https://www.google.com/search?q=weather+today";
    document.documentElement.classList.add("is-leaving");
    document.title = "Weather";
    try { window.location.replace(url); } catch (e) { window.location.href = url; }
  }
  if (exitLink) { exitLink.addEventListener("click", quickExit); }
  var lastEsc = 0;
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") { return; }
    var now = Date.now();
    if (now - lastEsc < 1000) { quickExit(); }
    lastEsc = now;
  });

  /* 2. AGE CHOICE on "What to do first"
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

  /* 3. Close the help sheet or the menu when someone taps outside it. */
  document.addEventListener("click", function (event) {
    var open = document.querySelectorAll(".helpbar__help[open], .menu[open]");
    Array.prototype.forEach.call(open, function (d) {
      if (!d.contains(event.target)) { d.removeAttribute("open"); }
    });
  });
})();
