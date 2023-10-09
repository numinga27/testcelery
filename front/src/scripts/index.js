import "../styles/main.css";
import "../styles/media.css";
import "../fonts/fonts.css";
import "../styles/header.css";

import { startFetchingWithInterval } from "./datafetch";
import { toggleEventVisibility, toggleStarColor } from "./changeStyle";
import { stopUpdate } from "./header";

const headerMenu = document.querySelector(".header-menu");
const content = document.querySelector("#content");

const currentTournaments = [];

// const footballLink = "http://localhost:8000/testing/api/live/football"; //для локального сервака
// const hockeyLink = "http://localhost:8000/testing/api/live/hockey"; //для локального сервака

const footballLink = "/testing/api/live/football"; //для обычного сервака
const hockeyLink = "/testing/api/live/hockey"; //для обычного сервака

headerMenu.addEventListener("click", stopUpdate);
content.addEventListener("click", toggleEventVisibility);
content.addEventListener("click", toggleStarColor);

export { headerMenu, footballLink, hockeyLink, content, currentTournaments };

if (window.location.href.indexOf("football.html") !== -1) {
  startFetchingWithInterval(footballLink);
} else if (window.location.href.indexOf("hockey.html") !== -1) {
  startFetchingWithInterval(hockeyLink);
} else {
  console.error("Неизвестная страница");
}

document.cookie = "user_id=12345; samesite=lax";