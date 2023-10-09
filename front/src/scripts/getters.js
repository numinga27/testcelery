function getSportCategory() {
  switch (content.dataset.type) {
    case "hockey":
      return "hockey";
      break;
    case "football":
      return "football";
      break;
  }
}

function getImageLink(string) {
  const link = string.replace(/[\[\]']/g, "");
  return link;
}

function getGameTime(eventUnixTime) {
  const currentUnixTime = Math.floor(Date.now() / 1000);
  const timeDifference = currentUnixTime - eventUnixTime;
  const minutes = Math.floor(timeDifference / 60);
  return minutes;
}

function getCriterion() {
  const sport = getSportCategory();
  if (sport === 'football') {
    return 'event_id'
  } else {
    return 'events_id'
  }
}

export { getGameTime, getSportCategory, getImageLink, getCriterion };