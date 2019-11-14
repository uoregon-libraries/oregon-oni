document.addEventListener("DOMContentLoaded", init, false)

function init() {
  // This is so awful, but it's the only easy way to get focus boxes to
  // properly wrap all the different elements we need wrapped - e.g., when we
  // have an <a> around an <img>, for some reason it doesn't work to just have
  // simple CSS rules to show focus on the <a>: we get focus boxes that are the
  // wrong size, or behind images, etc.
  addFocusableToAll(document.querySelectorAll("a"));

  // Hack in the focusable class to all <th> tags for our tablesorter mess
  var els = document.querySelectorAll("th");
  for (var i = 0; i < els.length; i++) {
    els[i].classList.add("focusable");
  }
}

function addFocusableToAll(els) {
  for (var i = 0; i < els.length; i++) {
    addFocusable(els[i]);
  }
}

function addFocusable(e) {
  if (e.children.length > 0) {
    addFocusableToAll(e.children);
    return;
  }

  e.classList.add("focusable");
}
