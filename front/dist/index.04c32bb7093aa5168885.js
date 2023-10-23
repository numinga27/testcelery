/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  Yn: () => (/* binding */ currentTournaments)
});

// UNUSED EXPORTS: content, footballLink, headerMenu, hockeyLink

;// CONCATENATED MODULE: ./src/scripts/getters.js
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
  var link = string.replace(/[\[\]']/g, "");
  return link;
}
function getGameTime(eventUnixTime) {
  var currentUnixTime = Math.floor(Date.now() / 1000);
  var timeDifference = currentUnixTime - eventUnixTime;
  var minutes = Math.floor(timeDifference / 60);
  return minutes;
}
function getCriterion() {
  var sport = getSportCategory();
  if (sport === 'football') {
    return 'event_id';
  } else {
    return 'events_id';
  }
}

;// CONCATENATED MODULE: ./src/scripts/eventConstructor.js

function buildTournamentRow(tournament) {
  var tournamentRow = document.createElement("div");
  var sport = getSportCategory();
  tournamentRow.className = "tournament";
  tournamentRow.dataset.id = tournament.TOURNAMENT_TEMPLATE_ID;
  tournamentRow.append(buildTournamentHeader(tournament), buildEventsList(tournament.events, tournament.TOURNAMENT_TEMPLATE_ID, sport));
  return tournamentRow;
}
function buildTournamentHeader(event) {
  var tournamentHeader = document.createElement("div");
  tournamentHeader.className = "tournament__header";
  tournamentHeader.innerHTML = "\n      <img src=\"./icons/inactive_star.svg\" alt=\"add to favorites\" class=\"star inactive\">\n      <img src=\"".concat(event.tournament_imng, "\" alt=\"tournament_image\" class=\"tournament__icon\">\n      <p class=\"tournament__name\">").concat(event.name, "</p>\n      <img src=\"./icons/expand_btn.svg\" alt=\"expand game\" class=\"switch__btn\">\n    ");
  return tournamentHeader;
}
function buildEventsList(events, id, sport) {
  var eventsList = document.createElement("div");
  eventsList.className = "events__list";
  eventsList.setAttribute("data-eventsId", id);
  if (sport === "hockey") {
    events.forEach(function (event) {
      var eventWrapper = buildHockeyGame(event);
      eventsList.append(eventWrapper);
    });
  } else {
    events.forEach(function (event) {
      var eventWrapper = buildFootballGame(event);
      eventsList.append(eventWrapper);
    });
  }
  return eventsList;
}
function buildFootballGame(event) {
  var eventWrapper = document.createElement("div");
  eventWrapper.className = "event__game";
  eventWrapper.setAttribute("data-id", "".concat(event.event_id));
  eventWrapper.append(buildCheckBox(event.event_id), buildFavStar(), buildEventTime(event.start_time), buildTeamsBlock(event), buildFootballScore(event, "current__score"), buildFootballScore(event, "first"), buildFootballScore(event, "second"));
  return eventWrapper;
}
function buildHockeyGame(event) {
  var eventWrapper = document.createElement("div");
  eventWrapper.className = "event__game";
  eventWrapper.setAttribute("data-id", "".concat(event.events_id));
  eventWrapper.append(buildCheckBox(event.events_id), buildFavStar(), buildEventStage(event.stage, event.game_time), buildTeamsBlock(event), buildHockeyScore(event, "current__score"), buildHockeyScore(event, "first"), buildHockeyScore(event, "second"), buildHockeyScore(event, "third"));
  return eventWrapper;
}
function buildTeamsBlock(event) {
  var block = document.createElement("div");
  block.className = "teams__block";
  block.append(buildTeamString(event, "home"), buildTeamString(event, "away"));
  return block;
}
function buildTeamString(event, status) {
  var teamString = document.createElement("div");
  teamString.className = "team ".concat(status);
  switch (status) {
    case "home":
      teamString.append(buildTeamImg(event.home_images, status), buildTeamName(event.home_name, status));
      break;
    case "away":
      teamString.append(buildTeamImg(event.away_images, status), buildTeamName(event.away_name, status));
      break;
  }
  return teamString;
}
function buildCheckBox(id) {
  var checkbox = document.createElement("div");
  checkbox.innerHTML = "\n      <input type=\"checkbox\" class=\"custom__checkbox\" id=\"game".concat(id, "\"/>\n      <label for=\"game").concat(id, "\"></label>\n    ");
  return checkbox;
}
function buildFavStar() {
  var favStar = document.createElement("img");
  favStar.className = "star inactive";
  favStar.setAttribute("src", "./icons/inactive_star.svg");
  favStar.setAttribute("alt", "add to favorites");
  return favStar;
}
function buildEventTime(unixTime) {
  var time = document.createElement("p");
  time.className = "event__time";
  time.innerText = getGameTime(unixTime);
  return time;
}
function buildHockeyTime(gametime) {
  var time = document.createElement("p");
  time.className = "event__time";
  time.innerText = gametime;
  return time;
}
function buildEventStage(stage, time) {
  var stageWrapper = document.createElement("div");
  stageWrapper.className = "hockey__stage";
  if (stage === "PAUSE") {
    stageWrapper.append(transformHockeyStage(stage));
  } else {
    stageWrapper.append(transformHockeyStage(stage), buildHockeyTime(time));
  }
  return stageWrapper;
}
function transformHockeyStage(stage) {
  var eventStage = document.createElement("p");
  eventStage.className = "stage";
  switch (stage) {
    case "FIRST_PERIOD":
      eventStage.innerHTML = '<span class="full">1st Period</span> <span class="short">P1</span>';
      break;
    case "SECOND_PERIOD":
      eventStage.innerHTML = '<span class="full">2nd Period</span> <span class="short">P2</span>';
      break;
    case "THIRD_PERIOD":
      eventStage.innerHTML = '<span class="full">3rd Period</span> <span class="short">P3</span>';
      break;
    case "PAUSE":
      eventStage.innerHTML = '<span class="full">Break Time</span> <span class="short">Pause</span>';
      break;
  }
  return eventStage;
}
function buildTeamName(teamname, status) {
  var name = document.createElement("p");
  name.className = "team__name";
  name.classList.add(status);
  name.innerText = teamname;
  return name;
}
function buildTeamImg(link, status) {
  var teamImg = document.createElement("img");
  var imgLink = getImageLink(link);
  teamImg.className = "team__img";
  teamImg.classList.add(status);
  teamImg.setAttribute("src", imgLink);
  return teamImg;
}
function buildFootballScore(event, part) {
  var score = document.createElement("p");
  switch (part) {
    case "current__score":
      score.className = "current__score";
      score.innerHTML = "\n          <p>".concat(event.home_score_current, "</p>\n          <p>").concat(event.away_score_current, "</p>\n        ");
      break;
    case "first":
      score.className = "time__score first";
      score.innerText = "".concat(event.home_score_part_1, ":").concat(event.away_score_part_1);
      break;
    case "second":
      score.className = "time__score second";
      var homeScore = event.home_score_current - event.home_score_part_1;
      var awayScore = event.away_score_current - event.away_score_part_1;
      score.innerText = "".concat(homeScore, ":").concat(awayScore);
      break;
  }
  return score;
}
function buildHockeyScore(event, part) {
  var score = document.createElement("p");
  switch (part) {
    case "current__score":
      score.className = "current__score";
      score.innerHTML = "\n          <p>".concat(event.home_current_score, "</p>\n\n          <p>").concat(event.away_current_score, "</p>\n        ");
      break;
    case "first":
      score.className = "time__score first";
      score.innerText = "".concat(event.home_current_score - event.home_score_part_2 - event.home_score_part_3, ":").concat(event.away_current_score - event.away_score_part_2 - event.away_score_part_3);
      break;
    case "second":
      score.className = "time__score second";
      score.innerText = "".concat(event.home_current_score - event.home_score_part_1 - event.home_score_part_3, ":").concat(event.away_current_score - event.away_score_part_1 - event.away_score_part_3);
      break;
    case "third":
      score.className = "time__score third";
      score.innerText = "".concat(event.home_current_score - event.home_score_part_1 - event.home_score_part_2, ":").concat(event.away_current_score - event.away_score_part_1 - event.away_score_part_2);
      break;
  }
  return score;
}

;// CONCATENATED MODULE: ./src/scripts/changeStyle.js
function highlightEvent(evt) {
  evt.classList.add("highlighted");
  setTimeout(function () {
    evt.classList.remove("highlighted");
  }, 60000);
}
function toggleEventVisibility(_ref) {
  var target = _ref.target;
  if (target.classList.contains("switch__btn")) {
    var evtsList = target.closest(".tournament").lastElementChild;
    target.classList.toggle("hide");
    evtsList.classList.toggle("hide");
  }
}
function toggleStarColor(_ref2) {
  var target = _ref2.target;
  if (target.classList.contains("star") && target.classList.contains("inactive")) {
    target.classList.remove("inactive");
    target.classList.add("active");
    target.setAttribute("src", "./icons/active_star.svg");
  } else if (target.classList.contains("star") && target.classList.contains("active")) {
    target.classList.remove("active");
    target.classList.add("inactive");
    target.setAttribute("src", "./icons/inactive_star.svg");
  }
}
function showGoal(event, status) {
  var scoringTeam = event.querySelector(".team.".concat(status));
  scoringTeam.classList.add("scoring");
  setTimeout(function () {
    scoringTeam.classList.remove("scoring");
  }, 60000);
}

;// CONCATENATED MODULE: ./src/scripts/liveUpdate.js



function addNewEvents(currEvts, newEvts, tournamentId) {
  newEvts.forEach(function (event, index) {
    var foundEvent = findEvent(currEvts, "event_id", event);
    var sport = getSportCategory();
    if (!foundEvent && sport === "football") {
      currEvts.splice(index, 0, event);
      var eventRow = buildFootballGame(event);
      var eventsList = document.querySelector("[data-eventsId=\"".concat(tournamentId, "\"]"));
      var events = eventsList.children;
      eventsList.insertBefore(eventRow, events[index]);
    }
    if (!foundEvent && sport === "hockey") {
      currEvts.splice(index, 0, event);
      var _eventRow = buildHockeyGame(event);
      var _eventsList = document.querySelector("[data-eventsId=\"".concat(tournamentId, "\"]"));
      var _events = _eventsList.children;
      _eventsList.insertBefore(_eventRow, _events[index]);
    }
  });
}
function removeOldEvents(currEvts, newEvts) {
  var indexesToDelete = [];
  var criterion = getCriterion();
  currEvts.forEach(function (currEvt, idx) {
    var isNewEvent = findEvent(newEvts, criterion, currEvt);
    if (!isNewEvent) {
      var oldEvt = document.querySelector("[data-id=\"".concat(currEvt[criterion], "\"]"));
      oldEvt.remove();
      indexesToDelete.unshift(idx);
    }
  });
  indexesToDelete.forEach(function (idx) {
    currEvts.splice(idx, 1);
  });
}
function updateEvents(currEvts, newEvts) {
  var criterion = getCriterion();
  currEvts.forEach(function (currEvt) {
    var updatedEvt = findEvent(newEvts, criterion, currEvt);
    if (updatedEvt) {
      updateEventScore(currEvt, updatedEvt);
      updateStage(currEvt, updatedEvt);
    }
  });
}
function updateEventScore(currEvent, newEvent) {
  var idKey = getCriterion();
  var sport = getSportCategory();
  var event = document.querySelector("[data-id=\"".concat(currEvent[idKey], "\"]"));
  if (sport === "football") {
    compareFootballScore(event, currEvent, newEvent);
  }
  if (sport === "hockey") {
    compareHockeyScore(event, currEvent, newEvent);
  }
}
function updateStage(currEvent, newEvent) {
  var sport = getSportCategory();
  if (sport === "hockey" && currEvent.game_time !== newEvent.game_time) {
    currEvent.game_time = newEvent.game_time;
    currEvent.stage = newEvent.stage;
    var event = document.querySelector("[data-id=\"".concat(currEvent.events_id, "\"]"));
    var stageWrapper = event.querySelector(".hockey__stage");
    stageWrapper.innerHTML = "";
    stageWrapper.append(transformHockeyStage(currEvent.stage), buildHockeyTime(currEvent.game_time));
  }
}
function compareFootballScore(domEvt, currEvt, newEvt) {
  if (currEvt.home_score_current !== newEvt.home_score_current || currEvt.away_score_current !== newEvt.away_score_current) {
    var scoringTeam = determineScoringTeam(currEvt.home_score_current, newEvt.home_score_current);
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
  if (currEvt.home_current_score !== newEvt.home_current_score || currEvt.away_current_score !== newEvt.away_current_score) {
    var scoringTeam = determineScoringTeam(currEvt.home_current_score, newEvt.home_current_score);
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
  var replacedScore = domEvent.querySelector(".".concat(scoreClass));
  replacedScore.parentNode.replaceChild(buildFunc(currEvent, scoreClass), replacedScore);
}
function findEvent(searchLocation, criterion, comparedEvt) {
  var foundEvt = searchLocation.find(function (currEvt) {
    return currEvt[criterion] === comparedEvt[criterion];
  });
  return foundEvt;
}

;// CONCATENATED MODULE: ./src/scripts/renderLive.js



function renderLiveContent(games) {
  addNewTournaments(games);
  removeOldTournaments(games);
}
function addNewTournaments(tournaments) {
  tournaments.forEach(function (tournament, index) {
    var foundTournament = findEvent(currentTournaments, "TOURNAMENT_TEMPLATE_ID", tournament);
    if (!foundTournament) {
      currentTournaments.splice(index, 0, tournament);
      var tournamentRow = buildTournamentRow(tournament);
      var tournirs = content.children;
      content.insertBefore(tournamentRow, tournirs[index]);
    } else {
      addNewEvents(foundTournament.events, tournament.events, tournament.TOURNAMENT_TEMPLATE_ID);
      removeOldEvents(foundTournament.events, tournament.events);
      updateEvents(foundTournament.events, tournament.events);
    }
  });
}
function removeOldTournaments(tournaments) {
  // позже добавить проверку на пустой event list
  var tournamentsToDelete = [];
  currentTournaments.forEach(function (tournament, index) {
    var targetId = tournament.TOURNAMENT_TEMPLATE_ID;
    var indexToDelete = tournaments.findIndex(function (currTournament) {
      return currTournament.TOURNAMENT_TEMPLATE_ID === targetId;
    });
    if (indexToDelete === -1) {
      tournamentsToDelete.unshift(index);
      var oldTournament = document.querySelector("[data-id=\"".concat(targetId, "\"]"));
      if (oldTournament) {
        oldTournament.remove();
      }
    }
  });
  tournamentsToDelete.forEach(function (index) {
    currentTournaments.splice(index, 1);
  });
}

;// CONCATENATED MODULE: ./src/scripts/datafetch.js
function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
var _getData;
function _regeneratorRuntime() { "use strict"; /*! regenerator-runtime -- Copyright (c) 2014-present, Facebook, Inc. -- license (MIT): https://github.com/facebook/regenerator/blob/main/LICENSE */ _regeneratorRuntime = function _regeneratorRuntime() { return e; }; var t, e = {}, r = Object.prototype, n = r.hasOwnProperty, o = Object.defineProperty || function (t, e, r) { t[e] = r.value; }, i = "function" == typeof Symbol ? Symbol : {}, a = i.iterator || "@@iterator", c = i.asyncIterator || "@@asyncIterator", u = i.toStringTag || "@@toStringTag"; function define(t, e, r) { return Object.defineProperty(t, e, { value: r, enumerable: !0, configurable: !0, writable: !0 }), t[e]; } try { define({}, ""); } catch (t) { define = function define(t, e, r) { return t[e] = r; }; } function wrap(t, e, r, n) { var i = e && e.prototype instanceof Generator ? e : Generator, a = Object.create(i.prototype), c = new Context(n || []); return o(a, "_invoke", { value: makeInvokeMethod(t, r, c) }), a; } function tryCatch(t, e, r) { try { return { type: "normal", arg: t.call(e, r) }; } catch (t) { return { type: "throw", arg: t }; } } e.wrap = wrap; var h = "suspendedStart", l = "suspendedYield", f = "executing", s = "completed", y = {}; function Generator() {} function GeneratorFunction() {} function GeneratorFunctionPrototype() {} var p = {}; define(p, a, function () { return this; }); var d = Object.getPrototypeOf, v = d && d(d(values([]))); v && v !== r && n.call(v, a) && (p = v); var g = GeneratorFunctionPrototype.prototype = Generator.prototype = Object.create(p); function defineIteratorMethods(t) { ["next", "throw", "return"].forEach(function (e) { define(t, e, function (t) { return this._invoke(e, t); }); }); } function AsyncIterator(t, e) { function invoke(r, o, i, a) { var c = tryCatch(t[r], t, o); if ("throw" !== c.type) { var u = c.arg, h = u.value; return h && "object" == _typeof(h) && n.call(h, "__await") ? e.resolve(h.__await).then(function (t) { invoke("next", t, i, a); }, function (t) { invoke("throw", t, i, a); }) : e.resolve(h).then(function (t) { u.value = t, i(u); }, function (t) { return invoke("throw", t, i, a); }); } a(c.arg); } var r; o(this, "_invoke", { value: function value(t, n) { function callInvokeWithMethodAndArg() { return new e(function (e, r) { invoke(t, n, e, r); }); } return r = r ? r.then(callInvokeWithMethodAndArg, callInvokeWithMethodAndArg) : callInvokeWithMethodAndArg(); } }); } function makeInvokeMethod(e, r, n) { var o = h; return function (i, a) { if (o === f) throw new Error("Generator is already running"); if (o === s) { if ("throw" === i) throw a; return { value: t, done: !0 }; } for (n.method = i, n.arg = a;;) { var c = n.delegate; if (c) { var u = maybeInvokeDelegate(c, n); if (u) { if (u === y) continue; return u; } } if ("next" === n.method) n.sent = n._sent = n.arg;else if ("throw" === n.method) { if (o === h) throw o = s, n.arg; n.dispatchException(n.arg); } else "return" === n.method && n.abrupt("return", n.arg); o = f; var p = tryCatch(e, r, n); if ("normal" === p.type) { if (o = n.done ? s : l, p.arg === y) continue; return { value: p.arg, done: n.done }; } "throw" === p.type && (o = s, n.method = "throw", n.arg = p.arg); } }; } function maybeInvokeDelegate(e, r) { var n = r.method, o = e.iterator[n]; if (o === t) return r.delegate = null, "throw" === n && e.iterator["return"] && (r.method = "return", r.arg = t, maybeInvokeDelegate(e, r), "throw" === r.method) || "return" !== n && (r.method = "throw", r.arg = new TypeError("The iterator does not provide a '" + n + "' method")), y; var i = tryCatch(o, e.iterator, r.arg); if ("throw" === i.type) return r.method = "throw", r.arg = i.arg, r.delegate = null, y; var a = i.arg; return a ? a.done ? (r[e.resultName] = a.value, r.next = e.nextLoc, "return" !== r.method && (r.method = "next", r.arg = t), r.delegate = null, y) : a : (r.method = "throw", r.arg = new TypeError("iterator result is not an object"), r.delegate = null, y); } function pushTryEntry(t) { var e = { tryLoc: t[0] }; 1 in t && (e.catchLoc = t[1]), 2 in t && (e.finallyLoc = t[2], e.afterLoc = t[3]), this.tryEntries.push(e); } function resetTryEntry(t) { var e = t.completion || {}; e.type = "normal", delete e.arg, t.completion = e; } function Context(t) { this.tryEntries = [{ tryLoc: "root" }], t.forEach(pushTryEntry, this), this.reset(!0); } function values(e) { if (e || "" === e) { var r = e[a]; if (r) return r.call(e); if ("function" == typeof e.next) return e; if (!isNaN(e.length)) { var o = -1, i = function next() { for (; ++o < e.length;) if (n.call(e, o)) return next.value = e[o], next.done = !1, next; return next.value = t, next.done = !0, next; }; return i.next = i; } } throw new TypeError(_typeof(e) + " is not iterable"); } return GeneratorFunction.prototype = GeneratorFunctionPrototype, o(g, "constructor", { value: GeneratorFunctionPrototype, configurable: !0 }), o(GeneratorFunctionPrototype, "constructor", { value: GeneratorFunction, configurable: !0 }), GeneratorFunction.displayName = define(GeneratorFunctionPrototype, u, "GeneratorFunction"), e.isGeneratorFunction = function (t) { var e = "function" == typeof t && t.constructor; return !!e && (e === GeneratorFunction || "GeneratorFunction" === (e.displayName || e.name)); }, e.mark = function (t) { return Object.setPrototypeOf ? Object.setPrototypeOf(t, GeneratorFunctionPrototype) : (t.__proto__ = GeneratorFunctionPrototype, define(t, u, "GeneratorFunction")), t.prototype = Object.create(g), t; }, e.awrap = function (t) { return { __await: t }; }, defineIteratorMethods(AsyncIterator.prototype), define(AsyncIterator.prototype, c, function () { return this; }), e.AsyncIterator = AsyncIterator, e.async = function (t, r, n, o, i) { void 0 === i && (i = Promise); var a = new AsyncIterator(wrap(t, r, n, o), i); return e.isGeneratorFunction(r) ? a : a.next().then(function (t) { return t.done ? t.value : a.next(); }); }, defineIteratorMethods(g), define(g, u, "Generator"), define(g, a, function () { return this; }), define(g, "toString", function () { return "[object Generator]"; }), e.keys = function (t) { var e = Object(t), r = []; for (var n in e) r.push(n); return r.reverse(), function next() { for (; r.length;) { var t = r.pop(); if (t in e) return next.value = t, next.done = !1, next; } return next.done = !0, next; }; }, e.values = values, Context.prototype = { constructor: Context, reset: function reset(e) { if (this.prev = 0, this.next = 0, this.sent = this._sent = t, this.done = !1, this.delegate = null, this.method = "next", this.arg = t, this.tryEntries.forEach(resetTryEntry), !e) for (var r in this) "t" === r.charAt(0) && n.call(this, r) && !isNaN(+r.slice(1)) && (this[r] = t); }, stop: function stop() { this.done = !0; var t = this.tryEntries[0].completion; if ("throw" === t.type) throw t.arg; return this.rval; }, dispatchException: function dispatchException(e) { if (this.done) throw e; var r = this; function handle(n, o) { return a.type = "throw", a.arg = e, r.next = n, o && (r.method = "next", r.arg = t), !!o; } for (var o = this.tryEntries.length - 1; o >= 0; --o) { var i = this.tryEntries[o], a = i.completion; if ("root" === i.tryLoc) return handle("end"); if (i.tryLoc <= this.prev) { var c = n.call(i, "catchLoc"), u = n.call(i, "finallyLoc"); if (c && u) { if (this.prev < i.catchLoc) return handle(i.catchLoc, !0); if (this.prev < i.finallyLoc) return handle(i.finallyLoc); } else if (c) { if (this.prev < i.catchLoc) return handle(i.catchLoc, !0); } else { if (!u) throw new Error("try statement without catch or finally"); if (this.prev < i.finallyLoc) return handle(i.finallyLoc); } } } }, abrupt: function abrupt(t, e) { for (var r = this.tryEntries.length - 1; r >= 0; --r) { var o = this.tryEntries[r]; if (o.tryLoc <= this.prev && n.call(o, "finallyLoc") && this.prev < o.finallyLoc) { var i = o; break; } } i && ("break" === t || "continue" === t) && i.tryLoc <= e && e <= i.finallyLoc && (i = null); var a = i ? i.completion : {}; return a.type = t, a.arg = e, i ? (this.method = "next", this.next = i.finallyLoc, y) : this.complete(a); }, complete: function complete(t, e) { if ("throw" === t.type) throw t.arg; return "break" === t.type || "continue" === t.type ? this.next = t.arg : "return" === t.type ? (this.rval = this.arg = t.arg, this.method = "return", this.next = "end") : "normal" === t.type && e && (this.next = e), y; }, finish: function finish(t) { for (var e = this.tryEntries.length - 1; e >= 0; --e) { var r = this.tryEntries[e]; if (r.finallyLoc === t) return this.complete(r.completion, r.afterLoc), resetTryEntry(r), y; } }, "catch": function _catch(t) { for (var e = this.tryEntries.length - 1; e >= 0; --e) { var r = this.tryEntries[e]; if (r.tryLoc === t) { var n = r.completion; if ("throw" === n.type) { var o = n.arg; resetTryEntry(r); } return o; } } throw new Error("illegal catch attempt"); }, delegateYield: function delegateYield(e, r, n) { return this.delegate = { iterator: values(e), resultName: r, nextLoc: n }, "next" === this.method && (this.arg = t), y; } }, e; }
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }
function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function startFetchingWithInterval(link) {
  getData(link);
  setInterval(function () {
    return getData(link);
  }, 5000);
}
function getData(_x) {
  return (_getData = _getData || _asyncToGenerator( /*#__PURE__*/_regeneratorRuntime().mark(function _callee(serverlink) {
    return _regeneratorRuntime().wrap(function _callee$(_context) {
      while (1) switch (_context.prev = _context.next) {
        case 0:
          _context.next = 2;
          return fetch(serverlink).then(function (response) {
            return response.json();
          }).then(function (data) {
            return renderLiveContent(data);
          })["catch"](function (error) {
            return console.error("Error fetching data:", error);
          });
        case 2:
        case "end":
          return _context.stop();
      }
    }, _callee);
  }))).apply(this, arguments);
}

;// CONCATENATED MODULE: ./src/scripts/header.js
function stopUpdate(evt) {
  if (evt.target.closest(".active__link")) {
    evt.preventDefault();
  }
}

;// CONCATENATED MODULE: ./src/scripts/index.js







var headerMenu = document.querySelector(".header-menu");
var scripts_content = document.querySelector("#content");
var currentTournaments = [];
var footballLink = "http://localhost:8000/testing/api/live/football";
var hockeyLink = "http://localhost:8000/testing/api/live/hockey";
headerMenu.addEventListener("click", stopUpdate);
scripts_content.addEventListener("click", toggleEventVisibility);
scripts_content.addEventListener("click", toggleStarColor);

if (window.location.href.indexOf("football.html") !== -1) {
  startFetchingWithInterval(footballLink);
} else if (window.location.href.indexOf("hockey.html") !== -1) {
  startFetchingWithInterval(hockeyLink);
} else {
  console.error("Неизвестная страница");
}
document.cookie = "user_id=12345; samesite=lax";
/******/ })()
;