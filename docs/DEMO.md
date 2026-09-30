# Demoablauf für ein Bewerbungsgespräch

Ungefähr drei Minuten. Dies ist ein Ablaufplan, kein bereits aufgezeichnetes Video.

## 0:00 bis 0:30 - Problem und Ziel

Erkläre den fiktiven Anwendungsfall: Mitarbeitende brauchen verständliche Antworten auf wiederkehrende IT-Fragen. Ziel ist ein prüfbarer Quellenabruf und optional ein sprachlicher Entwurf.

## 0:30 bis 1:15 - Erfolgreiche Suche

Frage „Wie richte ich VPN ein?“ eingeben. Zeige Originalauszug, Quellen-ID und aufklappbare Quelle. Erkläre, warum die Baseline zunächst ohne Modell funktioniert.

## 1:15 bis 1:45 - Bewusste Grenze

Frage „Wie hoch ist mein Gehalt?“ eingeben. Zeige die Zurückweisung. Das System kennt keine Gehaltsdaten und versucht keine Antwort zu erfinden.

## 1:45 bis 2:15 - Evaluation

Qualitätsansicht öffnen. Erkläre Quellen-Recall und Zurückweisung unbekannter Fragen. Weise darauf hin, dass 30 Entwicklungsfragen kein unabhängiger Qualitätsnachweis sind.

## 2:15 bis 3:00 - KI-Integration und nächste Entscheidung

Bei eingerichtetem Ollama den lokalen Modellmodus zeigen und Formulierung mit dem Originalauszug vergleichen. Andernfalls transparent erklären, dass die Integration mit simulierten Antworten getestet wurde, aber ein echter Modelllauf noch aussteht.

Als sinnvolle nächste Arbeit: unabhängige Fragen sammeln, Modellantworten bewerten und erst anhand der Ergebnisse über Embedding-Suche entscheiden.

## Fragen, die du erklären können solltest

- Warum reichen gültige Quellen-IDs nicht als Beweis für eine korrekte KI-Antwort?
- Warum ist ein Retrieval-Score keine Konfidenzwahrscheinlichkeit?
- Wie verhindert der Assistent erfundene Angaben bei unbekannten Themen?
- Was passiert bei einem Modellfehler?
- Welche Änderungen würden echte Unternehmensdaten und mehrere Nutzer erfordern?
