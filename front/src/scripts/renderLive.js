import { currentTournaments } from "./index";
import { buildTournamentRow } from "./eventConstructor";
import { addNewEvents, removeOldEvents, updateEvents, findEvent } from "./liveUpdate";


function renderLiveContent(games) {
  addNewTournaments(games);
  removeOldTournaments(games);
}

function addNewTournaments(tournaments) {
  tournaments.forEach((tournament, index) => {
    const foundTournament = findEvent(
      currentTournaments,
      "TOURNAMENT_TEMPLATE_ID",
      tournament
    );
    if (!foundTournament) {
      currentTournaments.splice(index, 0, tournament);
      const tournamentRow = buildTournamentRow(tournament);
      const tournirs = content.children;
      content.insertBefore(tournamentRow, tournirs[index]);
    } else {
      addNewEvents(
        foundTournament.events,
        tournament.events,
        tournament.TOURNAMENT_TEMPLATE_ID
      );
      removeOldEvents(foundTournament.events, tournament.events);
      updateEvents(foundTournament.events, tournament.events);
    }
  });
}

function removeOldTournaments(tournaments) { // позже добавить проверку на пустой event list
  const tournamentsToDelete = [];
  currentTournaments.forEach((tournament, index) => {
    const targetId = tournament.TOURNAMENT_TEMPLATE_ID;
    const indexToDelete = tournaments.findIndex(
      (currTournament) => currTournament.TOURNAMENT_TEMPLATE_ID === targetId
    );
    if (indexToDelete === -1) {
      tournamentsToDelete.unshift(index);
      const oldTournament = document.querySelector(`[data-id="${targetId}"]`);
      if (oldTournament) {
        oldTournament.remove();
      }
    }
  });
  tournamentsToDelete.forEach((index) => {
    currentTournaments.splice(index, 1);
  });
}

export { renderLiveContent };
