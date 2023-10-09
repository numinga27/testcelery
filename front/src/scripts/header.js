function stopUpdate(evt) {
  if (evt.target.closest(".active__link")) {
    evt.preventDefault();
  }
}

export { stopUpdate };
