import { renderLiveContent } from "./renderLive";


function startFetchingWithInterval(link) {
  getData(link);
  setInterval(() => getData(link), 5000);
}

async function getData(serverlink) {
  // заменить на вебсокет
  await fetch(serverlink)
    .then((response) => response.json())
    .then((data) => renderLiveContent(data))
    .catch((error) => console.error("Error fetching data:", error));
}

export { startFetchingWithInterval, getData };
