function turnOffAlarm() {
  fetch("/turnOffAlarm", { method: "POST" })
    .then((response) => response.text())
    .then((message) => alert(message))
    .catch((error) => console.error(error));
}
