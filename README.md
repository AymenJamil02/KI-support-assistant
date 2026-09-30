# Support Compass

**Ein deutscher Supportassistent, der interne IT-Informationen auffindbar macht und Antworten mit nachvollziehbaren Quellen vorbereitet.**

Portfolio-Projekt für den Aufgabenbereich KI Application Consulting: Anwendungsfall identifizieren, Werkzeug umsetzen, Ergebnisse prüfen und Anwender verständlich unterstützen. Alle Dokumente sind frei erfunden; dieses Projekt ist weder ein Auftrag noch eine Richtlinie eines Arbeitgebers.

## Was funktioniert?

- Deutsche Weboberfläche mit Beispiel-Fragen und aufklappbaren Quellen.
- Zwölf fiktive IT-Anleitungen: VPN, Passwort, MFA, Software, Zugriffsrechte, Phishing, Drucker, Meetings, Backup, Homeoffice, KI und Supporttickets.
- Lokale lexikalische Dokumentensuche mit BM25-Scoring, Stopwörtern und wenigen expliziten Synonymen.
- Quellenbasierte Originalauszüge ohne Modellinstallation als reproduzierbare Baseline.
- Optional: echte Antwortgenerierung mit einem lokal betriebenen Ollama-Sprachmodell.
- Klarer Rückfall auf Quellen-Auszüge, wenn das Modell fehlt, nicht erreichbar ist oder ungültige Quellen nennt.
- Qualitätsansicht mit 30 dokumentierten Entwicklungsfragen und einem gespeicherten Testbericht.
- 22 automatisierte Tests, einschließlich HTTP-Endpunkten und simulierten Modellfehlern.
- GitHub-Actions-Konfiguration für Python 3.11, 3.12 und 3.13.

## Schnellstart

Python **3.11 oder neuer** genügt. Für die Such-Baseline werden keine externen Python-Pakete benötigt.

```bash
git clone https://github.com/AymenJamil02/KI-support-assistant.git
cd KI-support-assistant
python -m portfolio.server
```

Alternativ den Projektordner aus der ZIP-Datei entpacken und dort den letzten Befehl ausführen.

Öffne anschließend **http://127.0.0.1:8765**. Unter Windows kannst du `start.ps1` in PowerShell ausführen, sofern deine vorhandene Ausführungsrichtlinie dies erlaubt. Der Server startet kein Browserfenster automatisch und endet mit Strg+C.

Beispiele:

- „Wie richte ich VPN ein?“
- „Ich habe eine Phishingmail bekommen.“
- „Wie hoch ist mein Gehalt?“ – hierfür fehlen Informationen, daher wird keine Fachantwort erfunden.

Bei belegtem Port: `python -m portfolio.server --port 8766`.

## Echte lokale KI-Antworten aktivieren

Die Standardansicht ist eine **Informationssuche mit Originalauszügen**, kein generatives Sprachmodell. Die KI-Option verwendet die lokale Ollama-Chat-API. Dafür müssen Ollama, ein passendes Modell und ausreichend Arbeitsspeicher vorhanden sein.

1. Ollama von [ollama.com](https://ollama.com/) installieren und den lokalen Dienst starten.
2. Ein für den eigenen Rechner geeignetes Chatmodell installieren; Hardwarebedarf und Modelllizenz beim Anbieter prüfen. Modellname aus `ollama list` übernehmen.
3. Den Modellnamen vor dem Start der Anwendung als Umgebungsvariable setzen:

```powershell
# Windows PowerShell: den Platzhalter durch den tatsächlich installierten Modellnamen ersetzen.
$env:OLLAMA_MODEL = 'dein-installiertes-modell'
python -m portfolio.server
```

```bash
# macOS / Linux
OLLAMA_MODEL=dein-installiertes-modell python -m portfolio.server
```

4. In der Oberfläche „Lokales Sprachmodell verwenden“ aktivieren.

`.env.example` erklärt die Variable; die Anwendung lädt `.env`-Dateien nicht automatisch. Es gibt keine bezahlten API-Aufrufe und keine API-Schlüssel. Die Anwendung sendet Frage und ausgewählte Quellen nur an `127.0.0.1:11434`; die Konfiguration des separat betriebenen Ollama-Dienstes liegt außerhalb dieser Anwendung.

**Verifiziert:** Modell-Anfrageformat, Fehlerbehandlung und Quellen-ID-Prüfung mit simulierten Antworten. **Noch nicht verifiziert:** echter Modelllauf und dessen fachliche Antwortqualität; im Entwicklungsumfeld war kein Ollama-Dienst erreichbar.

API-Referenz: [Ollama – Generate a chat message](https://docs.ollama.com/api/chat).

## Qualität selbst prüfen

```bash
python -m portfolio.evaluate
python -m unittest discover -s tests -v
```

Der erste Befehl aktualisiert `reports/evaluation.json`. Gemessen werden:

| Kennzahl | Definition |
|---|---|
| Quellen-Recall | Anteil der 24 beantwortbaren Fragen, deren erwartete Quelle unter den abgerufenen Quellen ist |
| Abstention-Rate | Anteil der sechs unbekannten Fragen, bei denen der Assistent keine passende Quelle behauptet |
| Antwortzeit | Lokale Laufzeit pro Frage, einschließlich lexikalischer Suche, ohne Modelllauf |

Im mitgelieferten Entwicklungsbericht bestehen 30 von 30 Fragen. Die Testmenge ist klein, handgeschrieben und zur Entwicklung genutzt: **Das ist kein unabhängiger Qualitätsnachweis.** Die Werte bewerten den Quellenabruf, nicht semantische Richtigkeit, Prompt-Injection-Resistenz oder generative Modellqualität.

Nach einer Erweiterung der Dokumente neue, bisher nicht verwendete Fragen ergänzen und Fehler analysieren. Für einen fairen Modellvergleich dieselben Fragen manuell anhand von Korrektheit, Quellenbezug, Vollständigkeit und verständlicher Sprache bewerten. Keine künstliche Zeitersparnis oder Nutzerstudie behaupten.

## Architektur

```text
Browser (HTML/CSS/JavaScript)
             |
       lokales HTTP-API
             |
    Frage prüfen und tokenisieren
             |
    BM25-Suche in Markdown-Dokumenten
             |
       passende Quelle?
       /             \
     nein            ja
     |               |
   Rückfrage     Originalauszug
                 oder optional
                 Ollama-Entwurf
                     |
             Quellen-ID-Prüfung
                     |
             menschliche Prüfung
```

Keine Embeddings, Vektordatenbank oder Agentenframeworks: Das Projekt startet mit einer verständlichen Baseline, deren Verhalten anhand konkreter Fragen überprüfbar ist. In einer Erweiterung lässt sich Embedding-Suche gegen denselben Evaluationsdatensatz vergleichen.

## Dateien

```text
portfolio/assistant.py  Suche, Quellen und Ollama-Anbindung
portfolio/server.py     HTTP-Endpunkte und statische Oberfläche
portfolio/evaluate.py   Reproduzierbare Evaluation
web/                    Deutsche Oberfläche
data/knowledge/         Zwölf fiktive Markdown-Dokumente
data/questions.json     30 Entwicklungsfragen mit erwarteten Quellen
reports/evaluation.json Gemessener Baseline-Bericht
tests/                  Unit- und API-Tests
docs/                   Anwendungsfall, Anleitung und Demoablauf
.github/workflows/      Automatische Tests nach GitHub-Upload
```

## Grenzen und verantwortliche Nutzung

- Die Demo hört ausschließlich auf dem eigenen Rechner und hat keine Benutzeranmeldung. Sie ist kein Produktionsserver.
- Weder Fragen noch Inhalte werden protokolliert oder in einer Datenbank gespeichert. Der Browser zeigt die letzte Antwort bis zum Neuladen.
- Lexikalische Suche kann Synonyme, lange Mehrthemenfragen und implizite Zusammenhänge verfehlen. Der Score ist keine Konfidenzwahrscheinlichkeit.
- Die Prüfung gültiger Quellen-IDs verhindert erfundene IDs, beweist aber nicht, dass jeder generierte Satz durch die Quelle gedeckt ist.
- Promptregeln sind keine vollständige Absicherung gegen Prompt Injection. Kein Werkzeug führt Aktionen in Unternehmenssystemen aus.
- Es gibt keine automatisierten Freigaben, Ticketversendungen oder Entscheidungen über Mitarbeitende.
- Die Demo enthält keine persönlichen Bewerbungsunterlagen, echten Unternehmensrichtlinien oder Zugangsdaten.

## Über die Entwicklung sprechen

Das Projekt wurde mit KI-Unterstützung erstellt. Für ein Bewerbungsgespräch die Architektur, Tests und Grenzen selbst nachvollziehen und eigene Änderungen belegen. Die Dokumentation unterscheidet implementierte Funktionen und verifizierte Resultate von optionaler Modellintegration und zukünftigen Erweiterungen.

## Lizenz

MIT, siehe `LICENSE`. Die fiktiven Beispieldokumente sind Teil des Projekts.
