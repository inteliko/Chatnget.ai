
/* Rich text Editor  JavaScript */

function formatText(command, value = null) {
  document.execCommand(command, false, value);
}

