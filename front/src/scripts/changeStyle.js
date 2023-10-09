function highlightEvent(evt) {
  evt.classList.add("highlighted");
  setTimeout(() => {
    evt.classList.remove("highlighted");
  }, 60000);
}

function toggleEventVisibility({ target }) {
  if (target.classList.contains("switch__btn")) {
    const evtsList = target.closest(".tournament").lastElementChild;
    target.classList.toggle("hide");
    evtsList.classList.toggle("hide");
  }
}

function toggleStarColor({ target }) {
  if (
    target.classList.contains("star") &&
    target.classList.contains("inactive")
  ) {
    target.classList.remove("inactive");
    target.classList.add("active");
    target.setAttribute("src", "./icons/active_star.svg");
  } else if (
    target.classList.contains("star") &&
    target.classList.contains("active")
  ) {
    target.classList.remove("active");
    target.classList.add("inactive");
    target.setAttribute("src", "./icons/inactive_star.svg");
  }
}

function showGoal(event, status) {
  const scoringTeam = event.querySelector(`.team.${status}`);
  scoringTeam.classList.add("scoring");
  setTimeout(() => {
    scoringTeam.classList.remove("scoring");
  }, 60000);

}

export { highlightEvent, toggleEventVisibility, toggleStarColor, showGoal };