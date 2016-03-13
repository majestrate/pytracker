



window.onload = function() {
  while (document.body.children.length) {
    document.body.removeChild(document.body.children[0]);
  }
  document.body.appendChild(document.createTextNode("you must disable javascript to view this site"));
}
