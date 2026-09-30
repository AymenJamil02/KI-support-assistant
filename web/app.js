"use strict";
const $ = id => document.getElementById(id);
const fmt = n => new Intl.NumberFormat("de-DE", {maximumFractionDigits: 1}).format(n);
const pct = n => `${fmt(n * 100)} %`;
let currentAnswer = "";
function element(tag, text, cls) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (cls) e.className = cls; return e; }
async function api(path, body) {
  const response = await fetch(path, body === undefined ? {} : {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Die Anfrage ist fehlgeschlagen.");
  return data;
}
function metrics(container, entries) {
  container.replaceChildren(...entries.map(([label, value, note]) => { const card = element("div", undefined, "metric"); card.append(element("div", label, "metric-label"), element("div", value, "metric-value"), element("div", note, "metric-note")); return card; }));
}
function row(values) { const tr = element("tr"); for (const value of values) { const td = element("td"); if (value instanceof Node) td.append(value); else td.textContent = value; tr.append(td); } return tr; }
function status(text, success) { return element("span", text, success ? "status" : "status amber"); }
function showTab(name) { for (const section of ["assistant", "evaluation"]) { $(section).hidden = section !== name; const button = $(`tab-${section}`); button.classList.toggle("active", section === name); button.setAttribute("aria-selected", String(section === name)); } }
for (const name of ["assistant", "evaluation"]) $(`tab-${name}`).addEventListener("click", () => showTab(name));
document.querySelectorAll("[data-question]").forEach(button => button.addEventListener("click", () => { $("question").value = button.dataset.question; $("question").focus(); }));
$("question-form").addEventListener("submit", async event => {
  event.preventDefault(); $("assistant-error").textContent = ""; $("ask").disabled = true; $("ask").textContent = "Wird geprüft …"; $("answer-card").hidden = true;
  try {
    const result = await api("/api/ask", {question: $("question").value, use_model: $("use-model").checked});
    currentAnswer = result.answer; $("answer-text").textContent = result.answer;
    $("answer-mode").textContent = result.abstained ? "KEINE PASSENDE QUELLE" : result.mode === "ollama" ? "KI-ENTWURF · MENSCHLICHE PRÜFUNG ERFORDERLICH" : "ORIGINALAUSZÜGE · KEINE GENERIERTE KI-ANTWORT";
    $("answer-warning").hidden = !result.warning; $("answer-warning").textContent = result.warning || "";
    $("sources").replaceChildren(...result.sources.map(source => { const d = element("details", undefined, "source"); d.append(element("summary", `${source.title} · ${source.id}`), element("p", source.text)); return d; }));
    $("answer-timing").textContent = `Bearbeitungszeit: ${fmt(result.elapsed_ms)} ms. Demo-Inhalte vor Verwendung prüfen.`; $("copy-status").textContent = ""; $("answer-card").hidden = false;
  } catch (error) { $("assistant-error").textContent = error.message; }
  finally { $("ask").disabled = false; $("ask").textContent = "Antwort finden ↗"; }
});
$("copy-answer").addEventListener("click", async () => { try { await navigator.clipboard.writeText(currentAnswer); $("copy-status").textContent = "Kopiert"; } catch { $("copy-status").textContent = "Bitte den Text markieren und manuell kopieren."; } });
async function documents() { try { const docs = await api("/api/documents"); $("document-list").replaceChildren(...docs.map(d => { const item = element("details", undefined, "doc-item"); item.append(element("summary", d.title), element("p", d.text)); return item; })); } catch (error) { $("assistant-error").textContent = error.message; } }
async function evaluation() { try { const r = await api("/api/evaluation"); metrics($("eval-metrics"), [["Testfragen", fmt(r.total), "24 bekannte · 6 unbekannte"], ["Erwartete Quelle enthalten", pct(r.source_recall), "Quellen-Recall"], ["Unbekannte Fragen abgewiesen", pct(r.unknown_abstention_rate), "Abstention-Rate"], ["Antwortzeit · Median", `${fmt(r.median_ms)} ms`, "Lokaler Testlauf"]]); $("eval-limitations").textContent = r.limitations; $("eval-results").replaceChildren(...r.results.map(test => row([test.question, test.source || "Keine Quelle", status(test.passed ? "Bestanden" : "Prüfen", test.passed)]))); } catch (error) { $("eval-error").textContent = error.message; } }
documents(); evaluation();
