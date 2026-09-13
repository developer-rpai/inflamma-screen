/* inflamma-screen web demo. Mirrors the Python engine scoring exactly:
   percent = round(100 * sum(weight * answer) / (2 * sum(weight)), 1)
   bands: <30 low, <=60 moderate, else elevated.
   Educational use only. Not a diagnostic tool. */

(function () {
  "use strict";

  var DATA = window.INFLAMMA_SCREEN_DATA.conditions;

  var DISCLAIMER =
    "Educational screening only. This is not a diagnosis. This tool is not " +
    "a medical device and cannot confirm or rule out any condition. Results " +
    "reflect how closely your answers match commonly described symptom " +
    "patterns. Please discuss your symptoms with a qualified clinician.";

  var ANSWER_LABELS = ["Never", "Sometimes", "Often"];

  var BAND_GUIDANCE = {
    low: "Your answers show limited overlap with commonly described patterns " +
      "for this condition. If symptoms persist or worry you, a clinician can " +
      "still help you understand them.",
    moderate: "Your answers show some overlap with commonly described patterns " +
      "for this condition. Consider writing down your symptoms and discussing " +
      "them with a clinician.",
    elevated: "Your answers show notable overlap with commonly described " +
      "patterns for this condition. Consider booking a clinician appointment " +
      "and bringing the generated summary with you."
  };

  var state = { step: "picker", conditionId: null, index: 0, answers: {} };
  var stepEl = document.getElementById("step");

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") { node.className = attrs[k]; }
        else { node.setAttribute(k, attrs[k]); }
      });
    }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }

  function focusHeading(container) {
    var h = container.querySelector("h2");
    if (h) {
      h.setAttribute("tabindex", "-1");
      h.focus({ preventScroll: false });
    }
  }

  function getCondition(id) {
    return DATA.filter(function (c) { return c.id === id; })[0];
  }

  function score(condition, answers) {
    var weighted = 0, maxWeighted = 0, endorsed = [];
    condition.questions.forEach(function (q) {
      var v = answers[q.id];
      if (v === undefined) { return; }
      weighted += q.weight * v;
      maxWeighted += q.weight * 2;
      if (q.key && v === 2) { endorsed.push(q.text); }
    });
    var percent = maxWeighted ? Math.round(1000 * weighted / maxWeighted) / 10 : 0;
    var band = percent < 30 ? "low" : (percent <= 60 ? "moderate" : "elevated");
    return { percent: percent, band: band, endorsed: endorsed };
  }

  function renderPicker() {
    state.step = "picker";
    stepEl.innerHTML = "";
    var card = el("div", { "class": "card" });
    card.appendChild(el("h2", { "class": "step-title" },
      "Which condition would you like to screen for?"));
    card.appendChild(el("p", null,
      "Answer 12 plain-language questions about commonly described symptom patterns."));
    var grid = el("div", { "class": "condition-grid", role: "group",
      "aria-label": "Choose a condition" });
    DATA.forEach(function (c) {
      var btn = el("button", { "class": "condition-card", type: "button" });
      btn.appendChild(el("h3", null, c.name));
      btn.appendChild(el("p", null, c.description));
      btn.addEventListener("click", function () {
        state.conditionId = c.id;
        state.index = 0;
        state.answers = {};
        renderQuestion();
      });
      grid.appendChild(btn);
    });
    card.appendChild(grid);
    stepEl.appendChild(card);
    focusHeading(card);
  }

  function renderQuestion() {
    state.step = "question";
    var condition = getCondition(state.conditionId);
    var questions = condition.questions;
    var q = questions[state.index];
    stepEl.innerHTML = "";

    var card = el("div", { "class": "card" });
    card.appendChild(el("h2", { "class": "step-title" },
      condition.name + " screening"));

    var progress = el("div", { "class": "progress", role: "progressbar",
      "aria-valuemin": "1", "aria-valuemax": String(questions.length),
      "aria-valuenow": String(state.index + 1),
      "aria-label": "Question progress" });
    var fill = el("div");
    fill.style.width = Math.round(100 * (state.index + 1) / questions.length) + "%";
    progress.appendChild(fill);
    card.appendChild(progress);
    card.appendChild(el("p", null,
      "Question " + (state.index + 1) + " of " + questions.length));

    var fieldset = el("fieldset");
    fieldset.appendChild(el("legend", { "class": "question-text" }, q.text));
    ANSWER_LABELS.forEach(function (label, value) {
      var wrap = el("label", { "class": "answer-option" });
      var input = el("input", { type: "radio", name: "answer", value: String(value) });
      if (state.answers[q.id] === value) { input.checked = true; }
      wrap.appendChild(input);
      wrap.appendChild(el("span", null, label));
      fieldset.appendChild(wrap);
    });
    card.appendChild(fieldset);

    var row = el("div", { "class": "button-row" });
    var back = el("button", { "class": "btn btn-secondary", type: "button" }, "Back");
    back.disabled = state.index === 0;
    back.addEventListener("click", function () {
      if (state.index === 0) { renderPicker(); } else { state.index -= 1; renderQuestion(); }
    });
    var next = el("button", { "class": "btn btn-primary", type: "button" },
      state.index === questions.length - 1 ? "See results" : "Next");
    next.disabled = state.answers[q.id] === undefined;
    next.addEventListener("click", function () {
      if (state.index === questions.length - 1) { renderResults(); }
      else { state.index += 1; renderQuestion(); }
    });
    fieldset.addEventListener("change", function (e) {
      state.answers[q.id] = parseInt(e.target.value, 10);
      next.disabled = false;
    });
    row.appendChild(back);
    row.appendChild(next);
    card.appendChild(row);

    stepEl.appendChild(card);
    focusHeading(card);
  }

  function renderResults() {
    state.step = "results";
    var condition = getCondition(state.conditionId);
    var result = score(condition, state.answers);
    stepEl.innerHTML = "";

    var card = el("div", { "class": "card" });
    card.appendChild(el("h2", { "class": "step-title" }, "Your screening result"));

    var badge = el("span", { "class": "band-badge band-" + result.band }, result.band);
    var headline = el("p");
    headline.appendChild(el("strong", null, condition.name + ": "));
    headline.appendChild(badge);
    headline.appendChild(document.createTextNode(" (" + result.percent + "/100)"));
    card.appendChild(headline);

    var bar = el("div", { "class": "score-bar", role: "img",
      "aria-label": "Score " + result.percent + " out of 100" });
    var barFill = el("div");
    barFill.style.width = result.percent + "%";
    bar.appendChild(barFill);
    card.appendChild(bar);

    card.appendChild(el("p", null, BAND_GUIDANCE[result.band]));

    if (result.endorsed.length) {
      card.appendChild(el("h3", null, "Key symptoms you endorsed"));
      var ul = el("ul", { "class": "endorsed-list" });
      result.endorsed.forEach(function (t) { ul.appendChild(el("li", null, t)); });
      card.appendChild(ul);
    }

    var note = el("div", { "class": "result-disclaimer" });
    note.appendChild(el("strong", null, "Disclaimer: "));
    note.appendChild(document.createTextNode(DISCLAIMER));
    card.appendChild(note);

    var row = el("div", { "class": "button-row" });
    var download = el("button", { "class": "btn btn-primary", type: "button" },
      "Download summary");
    download.addEventListener("click", function () {
      var text = buildSummary(condition, result);
      var blob = new Blob([text], { type: "text/plain" });
      var a = el("a", { href: URL.createObjectURL(blob), download: "screening-summary.txt" });
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    });
    var restart = el("button", { "class": "btn btn-secondary", type: "button" },
      "Start over");
    restart.addEventListener("click", renderPicker);
    row.appendChild(download);
    row.appendChild(restart);
    card.appendChild(row);

    stepEl.appendChild(card);
    focusHeading(card);
  }

  function buildSummary(condition, result) {
    var lines = [
      "Inflammatory Skin Condition Screening Summary",
      "Generated: " + new Date().toISOString().slice(0, 10) +
        " (educational tool, not a diagnosis)",
      "",
      "Condition screened: " + condition.name,
      "Result band: " + result.band.toUpperCase() +
        " (score " + result.percent + "/100)",
      "",
      BAND_GUIDANCE[result.band],
      ""
    ];
    if (result.endorsed.length) {
      lines.push("Key symptoms you endorsed:");
      result.endorsed.forEach(function (t) { lines.push("  - " + t); });
      lines.push("");
    }
    lines.push(
      "Questions you may want to ask your clinician:",
      "  - Could my symptoms match a chronic inflammatory skin condition?",
      "  - What details should I track about my symptoms before my next visit?",
      "  - Would a referral to a dermatologist be appropriate?",
      "",
      "Disclaimer:",
      DISCLAIMER
    );
    return lines.join("\n");
  }

  renderPicker();
})();
