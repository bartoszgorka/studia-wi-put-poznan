function isEmpty(field) {
  if (field.length === 0) {
    return true;
  } else {
    return false;
  }
}

function showElement(e) {
  document.getElementById(e).style.visibility = 'visible';
}

function hideElement(e) {
  document.getElementById(e).style.visibility = 'hidden';
}

function validate(form) {
  var toCheck = ["f_imie", "f_nazwisko", "f_ulica", "f_miasto"];
  var messages = ["Niepoprawne imię", "Niepoprawne nazwisko", "Brakująca ulica", "Brak miasta"];
  var response = true;

  for (var i = 0; i < toCheck.length; i++) {
    var field = form.elements[toCheck[i]];
    if (!checkStringAndFocus(field, messages[i])) {
      response = false;
    }
  }

  if (!checkEmailRegEx(form.elements["f_email"].value) || checkZIPCodeRegEx(form.elements["f_kod"].value)) {
    response = false;
  }

  return response;
}

function startTimer(fName) {
  window.setTimeout("clearError(" + fName + ")", 5000);
}

function clearError(object) {
  object.innerHTML = "";
}

function checkStringAndFocus(obj, msg) {
  var str = obj.value;
  var errorFieldName = "e_" + obj.name.substr(2, obj.name.length);
  if (isWhiteSpace(str) || isEmpty(str)) {
    element = document.getElementById(errorFieldName);
    addClass(obj, "wrong");
    element.innerHTML = msg;
    startTimer(errorFieldName);
    obj.focus();
    return false;
  } else {
    return true;
  }
}

function checkString(check, errorMessage) {
  var invalid = isEmpty(check) || isWhiteSpace(check);
  if (invalid) {
    alert(errorMessage);
  }
  return !invalid
}

function isWhiteSpace(str) {
  var ws = "\t\n\r ";
  for (var i = 0; i < str.length; i++) {
    var c = str.charAt(i);
    if (ws.indexOf(c) == -1) {
      return false;
    }
  }
  return true;
}

function checkEmail(str) {
  if (isWhiteSpace(str)) {
    alert("Podaj właściwy e-mail");
    return false;
  } else {
    var at = str.indexOf("@");
    if (at < 1) {
      alert("Nieprawidłowy e-mail");
      return false;
    } else {
      var l = -1;
      for (var i = 0; i < str.length; i++) {
        var c = str.charAt(i);
        if (c == ".") {
          l = i;
        }
      }
      if ((l < (at + 2)) || (l == str.length - 1)) {
        alert("Nieprawidłowy e-mail");
        return false;
      }
    }
    return true;
  }
}

function checkEmailRegEx(str) {
  var email = /[a-zA-Z_0-9\.]+@[a-zA-Z_0-9\.]+\.[a-zA-Z][a-zA-Z]+/;
  if (email.test(str))
    return true;
  else {
    alert("Podaj właściwy e-mail");
    return false;
  }
}

function hasClass(el, className) {
  if (el.classList)
    return el.classList.contains(className)
  else
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))
}

function addClass(el, className) {
  if (el.classList)
    el.classList.add(className)
  else if (!hasClass(el, className)) el.className += " " + className
}

function removeClass(el, className) {
  if (el.classList)
    el.classList.remove(className)
  else if (hasClass(el, className)) {
    var reg = new RegExp('(\\s|^)' + className + '(\\s|$)')
    el.className = el.className.replace(reg, ' ')
  }
}

function checkZIPCodeRegEx(str) {
  regex = /^[0-9]{2}-[0-9]{3}$/;
  var element = document.getElementById('kod');

  if (regex.test(str)) {
    removeClass(element, 'red');
    addClass(element, 'green');
    element.innerHTML = "OK";
    return false;
  } else {
    removeClass(element, 'green');
    addClass(element, 'red');
    element.innerHTML = "INCORRECT";
    return true;
  }
}

function alterRows(i, e) {
  if (e) {
    if (i % 2 == 1) {
      e.setAttribute("style", "background-color: Aqua;");
    }
    e = e.parentElement.nextElementSibling;
    if (e) {
      e = e.firstChild;
      alterRows(++i, e);
    }
  }
}

function nextNode(e) {
  while (e && e.nodeType != 1) {
    e = e.nextSibling;
  }
  return e;
}

function prevNode(e) {
  while (e && e.nodeType != 1) {
    e = e.previousSibling;
  }
  return e;
}

function swapRows(b) {
  var tab = prevNode(b.previousSibling);
  var tBody = nextNode(tab.firstChild);
  var lastNode = prevNode(tBody.lastChild);
  tBody.removeChild(lastNode);
  var firstNode = nextNode(tBody.firstChild);
  tBody.insertBefore(lastNode, firstNode);
}

function cnt(form, msg, maxSize) {
  if (form.value.length > maxSize)
    form.value = form.value.substring(0, maxSize);
  else
    msg.innerHTML = maxSize - form.value.length;
}

window.onload = function() {
  alterRows(1, (document.getElementsByTagName("td"))[0]);
}
