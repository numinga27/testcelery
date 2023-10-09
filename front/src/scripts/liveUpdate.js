import {
  buildFootballScore,
  buildHockeyScore,
  buildFootballGame,
  buildHockeyGame,
  buildHockeyTime,
  transformHockeyStage,
} from "./eventConstructor";
import { highlightEvent, showGoal } from "./changeStyle";
import { getSportCategory, getCriterion } from "./getters";

function addNewEvents(currEvts, newEvts, tournamentId) {
  newEvts.forEach((event, index) => {
    const foundEvent = findEvent(currEvts, "event_id", event);
    const sport = getSportCategory();
    if (!foundEvent && sport === "football") {
      currEvts.splice(index, 0, event);
      const eventRow = buildFootballGame(event);
      const eventsList = document.querySelector(
        `[data-eventsId="${tournamentId}"]`
      );
      const events = eventsList.children;
      eventsList.insertBefore(eventRow, events[index]);
    }

    if (!foundEvent && sport === "hockey") {
      currEvts.splice(index, 0, event);
      const eventRow = buildHockeyGame(event);
      const eventsList = document.querySelector(
        `[data-eventsId="${tournamentId}"]`
      );
      const events = eventsList.children;
      eventsList.insertBefore(eventRow, events[index]);
    }
  });
}

function removeOldEvents(currEvts, newEvts) {
  const indexesToDelete = [];
  const criterion = getCriterion();
  currEvts.forEach((currEvt, idx) => {
    const isNewEvent = findEvent(newEvts, criterion, currEvt);
    if (!isNewEvent) {
      const oldEvt = document.querySelector(
        `[data-id="${currEvt[criterion]}"]`
      );
      oldEvt.remove();
      indexesToDelete.unshift(idx);
    }
  });
  indexesToDelete.forEach((idx) => {
    currEvts.splice(idx, 1);
  });
}

function updateEvents(currEvts, newEvts) {
  const criterion = getCriterion();
  currEvts.forEach((currEvt) => {
    const updatedEvt = findEvent(newEvts, criterion, currEvt);
    if (updatedEvt) {
      updateEventScore(currEvt, updatedEvt);
      updateStage(currEvt, updatedEvt);
    }
  });
}

function updateEventScore(currEvent, newEvent) {
  const idKey = getCriterion();
  const sport = getSportCategory();
  const event = document.querySelector(`[data-id="${currEvent[idKey]}"]`);

  if (sport === "football") {
    compareFootballScore(event, currEvent, newEvent);
  }

  if (sport === "hockey") {
    compareHockeyScore(event, currEvent, newEvent);
  }
}

function updateStage(currEvent, newEvent) {
  const sport = getSportCategory();
  if (sport === "hockey" && currEvent.game_time !== newEvent.game_time) {
    currEvent.game_time = newEvent.game_time
    currEvent.stage = newEvent.stage;

    const event = document.querySelector(`[data-id="${currEvent.events_id}"]`);
    const stageWrapper = event.querySelector(".hockey__stage");
    stageWrapper.innerHTML = "";
    stageWrapper.append(
      transformHockeyStage(currEvent.stage),
      buildHockeyTime(currEvent.game_time)
    );
  }
}

function compareFootballScore(domEvt, currEvt, newEvt) {
  if (
    currEvt.home_score_current !== newEvt.home_score_current ||
    currEvt.away_score_current !== newEvt.away_score_current
  ) {
    const scoringTeam = determineScoringTeam(
      currEvt.home_score_current,
      newEvt.home_score_current
    );

    currEvt.home_score_current = newEvt.home_score_current;
    currEvt.away_score_current = newEvt.away_score_current;
    currEvt.home_score_part_1 = newEvt.home_score_part_1;
    currEvt.away_score_part_1 = newEvt.away_score_part_1;

    replaceScore(domEvt, "current__score", buildFootballScore, currEvt);
    replaceScore(domEvt, "first", buildFootballScore, currEvt);
    replaceScore(domEvt, "second", buildFootballScore, currEvt);

    showGoal(domEvt, scoringTeam);
    highlightEvent(domEvt);
  }
}

function compareHockeyScore(domEvt, currEvt, newEvt) {
  if (
    currEvt.home_current_score !== newEvt.home_current_score ||
    currEvt.away_current_score !== newEvt.away_current_score
  ) {
    const scoringTeam = determineScoringTeam(
      currEvt.home_current_score,
      newEvt.home_current_score
    );

    currEvt.home_current_score = newEvt.home_current_score;
    currEvt.away_current_score = newEvt.away_current_score;
    currEvt.home_score_part_1 = newEvt.home_score_part_1;
    currEvt.away_score_part_1 = newEvt.away_score_part_1;
    currEvt.home_score_part_2 = newEvt.home_score_part_2;
    currEvt.away_score_part_2 = newEvt.away_score_part_2;
    currEvt.home_score_part_3 = newEvt.home_score_part_3;
    currEvt.away_score_part_3 = newEvt.away_score_part_3;

    replaceScore(domEvt, "current__score", buildHockeyScore, currEvt);
    replaceScore(domEvt, "first", buildHockeyScore, currEvt);
    replaceScore(domEvt, "second", buildHockeyScore, currEvt);
    replaceScore(domEvt, "third", buildHockeyScore, currEvt);

    showGoal(domEvt, scoringTeam);
    highlightEvent(domEvt);
  }
}

function determineScoringTeam(currScore, newScore) {
  if (currScore !== newScore) {
    return "home";
  } else {
    return "away";
  }
}

function replaceScore(domEvent, scoreClass, buildFunc, currEvent) {
  const replacedScore = domEvent.querySelector(`.${scoreClass}`);
  replacedScore.parentNode.replaceChild(
    buildFunc(currEvent, scoreClass),
    replacedScore
  );
}

function findEvent(searchLocation, criterion, comparedEvt) {
  const foundEvt = searchLocation.find(
    (currEvt) => currEvt[criterion] === comparedEvt[criterion]
  );
  return foundEvt;
}

export { addNewEvents, removeOldEvents, updateEvents, findEvent };
