import { getGameTime, getSportCategory, getImageLink } from "./getters";

function buildTournamentRow(tournament) {
  const tournamentRow = document.createElement("div");
  const sport = getSportCategory();
  tournamentRow.className = "tournament";
  tournamentRow.dataset.id = tournament.TOURNAMENT_TEMPLATE_ID;

  tournamentRow.append(
    buildTournamentHeader(tournament),
    buildEventsList(tournament.events, tournament.TOURNAMENT_TEMPLATE_ID, sport)
  );

  return tournamentRow;
}

function buildTournamentHeader(event) {
  const tournamentHeader = document.createElement("div");
  tournamentHeader.className = "tournament__header";
  tournamentHeader.innerHTML = `
      <img src="./icons/inactive_star.svg" alt="add to favorites" class="star inactive">
      <img src="${event.tournament_imng}" alt="tournament_image" class="tournament__icon">
      <p class="tournament__name">${event.name}</p>
      <img src="./icons/expand_btn.svg" alt="expand game" class="switch__btn">
    `;
  return tournamentHeader;
}

function buildEventsList(events, id, sport) {
  let eventsList = document.createElement("div");
  eventsList.className = "events__list";
  eventsList.setAttribute("data-eventsId", id);

  if (sport === "hockey") {
    events.forEach((event) => {
      const eventWrapper = buildHockeyGame(event);
      eventsList.append(eventWrapper);
    });
  } else {
    events.forEach((event) => {
      const eventWrapper = buildFootballGame(event);
      eventsList.append(eventWrapper);
    });
  }

  return eventsList;
}

function buildFootballGame(event) {
  const eventWrapper = document.createElement("div");
  eventWrapper.className = "event__game";
  eventWrapper.setAttribute("data-id", `${event.event_id}`);
  eventWrapper.append(
    buildCheckBox(event.event_id),
    buildFavStar(),
    buildEventTime(event.start_time),
    buildTeamsBlock(event),
    buildFootballScore(event, "current__score"),
    buildFootballScore(event, "first"),
    buildFootballScore(event, "second")
  );
  return eventWrapper;
}

function buildHockeyGame(event) {
  const eventWrapper = document.createElement("div");
  eventWrapper.className = "event__game";
  eventWrapper.setAttribute("data-id", `${event.events_id}`);
  eventWrapper.append(
    buildCheckBox(event.events_id),
    buildFavStar(),
    buildEventStage(event.stage, event.game_time),
    buildTeamsBlock(event),
    buildHockeyScore(event, "current__score"),
    buildHockeyScore(event, "first"),
    buildHockeyScore(event, "second"),
    buildHockeyScore(event, "third")
  );
  return eventWrapper;
}

function buildTeamsBlock(event) {
  const block = document.createElement("div");
  block.className = "teams__block";
  block.append(buildTeamString(event, "home"), buildTeamString(event, "away"));
  return block;
}

function buildTeamString(event, status) {
  const teamString = document.createElement("div");
  teamString.className = `team ${status}`;
  switch (status) {
    case "home":
      teamString.append(
        buildTeamImg(event.home_images, status),
        buildTeamName(event.home_name, status)
      );
      break;
    case "away":
      teamString.append(
        buildTeamImg(event.away_images, status),
        buildTeamName(event.away_name, status)
      );
      break;
  }

  return teamString;
}

function buildCheckBox(id) {
  const checkbox = document.createElement("div");
  checkbox.innerHTML = `
      <input type="checkbox" class="custom__checkbox" id="game${id}"/>
      <label for="game${id}"></label>
    `;
  return checkbox;
}

function buildFavStar() {
  const favStar = document.createElement("img");
  favStar.className = "star inactive";
  favStar.setAttribute("src", "./icons/inactive_star.svg");
  favStar.setAttribute("alt", "add to favorites");
  return favStar;
}

function buildEventTime(unixTime) {
  const time = document.createElement("p");
  time.className = "event__time";
  time.innerText = getGameTime(unixTime);
  return time;
}

function buildHockeyTime(gametime) {
  const time = document.createElement("p");
  time.className = "event__time";
  time.innerText = gametime;
  return time;
}

function buildEventStage(stage, time) {
  const stageWrapper = document.createElement("div");
  stageWrapper.className = "hockey__stage";
  if (stage === "PAUSE") {
    stageWrapper.append(transformHockeyStage(stage));
  } else {
    stageWrapper.append(transformHockeyStage(stage), buildHockeyTime(time));
  }
  return stageWrapper;
}

function transformHockeyStage(stage) {
  const eventStage = document.createElement("p");
  eventStage.className = "stage";
  switch (stage) {
    case "FIRST_PERIOD":
      eventStage.innerHTML =
        '<span class="full">1st Period</span> <span class="short">P1</span>';
      break;
    case "SECOND_PERIOD":
      eventStage.innerHTML =
        '<span class="full">2nd Period</span> <span class="short">P2</span>';
      break;
    case "THIRD_PERIOD":
      eventStage.innerHTML =
        '<span class="full">3rd Period</span> <span class="short">P3</span>';
      break;
    case "PAUSE":
      eventStage.innerHTML =
        '<span class="full">Break Time</span> <span class="short">Pause</span>';
      break;
  }
  return eventStage;
}

function buildTeamName(teamname, status) {
  const name = document.createElement("p");
  name.className = "team__name";
  name.classList.add(status);
  name.innerText = teamname;
  return name;
}

function buildTeamImg(link, status) {
  const teamImg = document.createElement("img");
  const imgLink = getImageLink(link);
  teamImg.className = "team__img";
  teamImg.classList.add(status);
  teamImg.setAttribute("src", imgLink);
  return teamImg;
}

function buildFootballScore(event, part) {
  const score = document.createElement("p");
  switch (part) {
    case "current__score":
      score.className = "current__score";
      score.innerHTML = `
          <p>${event.home_score_current}</p>
          <p>${event.away_score_current}</p>
        `;
      break;
    case "first":
      score.className = "time__score first";
      score.innerText = `${event.home_score_part_1}:${event.away_score_part_1}`;
      break;
    case "second":
      score.className = "time__score second";
      const homeScore = event.home_score_current - event.home_score_part_1;
      const awayScore = event.away_score_current - event.away_score_part_1;
      score.innerText = `${homeScore}:${awayScore}`;
      break;
  }
  return score;
}

function buildHockeyScore(event, part) {
  const score = document.createElement("p");
  switch (part) {
    case "current__score":
      score.className = "current__score";
      score.innerHTML = `
          <p>${event.home_current_score}</p>

          <p>${event.away_current_score}</p>
        `;
      break;
    case "first":
      score.className = "time__score first";
      score.innerText = `${
        event.home_current_score -
        event.home_score_part_2 -
        event.home_score_part_3
      }:${
        event.away_current_score -
        event.away_score_part_2 -
        event.away_score_part_3
      }`;
      break;
    case "second":
      score.className = "time__score second";
      score.innerText = `${
        event.home_current_score -
        event.home_score_part_1 -
        event.home_score_part_3
      }:${
        event.away_current_score -
        event.away_score_part_1 -
        event.away_score_part_3
      }`;
      break;
    case "third":
      score.className = "time__score third";
      score.innerText = `${
        event.home_current_score -
        event.home_score_part_1 -
        event.home_score_part_2
      }:${
        event.away_current_score -
        event.away_score_part_1 -
        event.away_score_part_2
      }`;
      break;
  }
  return score;
}

export {
  buildTournamentRow,
  buildHockeyTime,
  buildFootballScore,
  buildHockeyScore,
  buildFootballGame,
  buildHockeyGame,
  transformHockeyStage
};
