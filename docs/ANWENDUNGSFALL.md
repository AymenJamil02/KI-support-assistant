# Anwendungsfall: interne IT-Fragen schneller einordnen

## Ausgangssituation

In einem fiktiven Unternehmen liegen IT-Anleitungen in einzelnen Dokumenten vor. Mitarbeitende müssen passende Informationen finden und entscheiden, wann sie den Support einschalten. Die Demo untersucht, ob Quellenabruf und ein optionaler Antwortentwurf diesen Ablauf verständlicher machen können.

Das ist eine angenommene Problemstellung, keine durch Interviews bei einem Arbeitgeber belegte Bedarfserhebung.

## Beteiligte und Anforderungen

| Rolle | Bedarf | Umgesetzte Funktion |
|---|---|---|
| Mitarbeitende | Eine verständliche Antwort auf eine konkrete Frage | Deutsche Oberfläche, Beispiele, Originalauszüge |
| Supportteam | Keine erfundenen Regeln oder unklaren Belege | Sichtbare Quellen, Zurückweisung unbekannter Themen |
| Fachverantwortliche | Inhalte kontrollieren und aktualisieren | Kleine, lesbare Markdown-Dokumente |
| Entwicklung | Fehler reproduzieren | Versionierte Fragen, Tests und Evaluationsbericht |

## Ablauf vor und mit der Demo

Vorher: Dokumente öffnen, Inhalte durchsuchen, passende Passage auswählen und in eigenen Worten zusammenfassen.

Mit der Demo: Frage eingeben, vorgeschlagene Quellen prüfen, optional Modell-Entwurf erstellen lassen und die Antwort fachlich kontrollieren. Bei fehlender Information den Support einschalten.

Eine messbare Zeitersparnis ist nicht nachgewiesen. Ein späterer Nutzertest sollte identische Aufgaben mit und ohne Assistent vergleichen, einschließlich Korrektheit und Zeitaufwand. Erst danach lässt sich ein Nutzen beziffern.

## Abnahmekriterien

- Bekannte Demo-Fragen liefern die erwartete Quelle.
- Fragen zu Gehalt, Urlaub oder Kantinenangebot lösen keine erfundene Antwort aus.
- In der Baseline stimmen angezeigte Antworten wörtlich mit Quelldokumenten überein.
- Ohne verfügbares Modell bleibt die Demo funktionsfähig und zeigt den Rückfall an.
- Eine generierte Antwort mit unbekannter Quellen-ID wird verworfen.
- Persönliche Bewerbungsunterlagen und Zugangsdaten sind nicht Bestandteil des Repositorys.

## Weiterentwicklung mit fachlicher Priorität

1. Neue Fragen unabhängig von der bisherigen Entwicklungsmenge erheben.
2. Mehrdeutige Fragen mit einer gezielten Rückfrage behandeln.
3. Modellantworten durch eine Person anhand dokumentierter Kriterien bewerten.
4. Synonymsuche und Embedding-Suche anhand derselben Aufgaben vergleichen.
5. Erst bei realem Einsatz: Identitätsprüfung, dokumentbezogene Zugriffsrechte, nachvollziehbare Datenfreigabe und ein geeigneter Produktionsserver.
