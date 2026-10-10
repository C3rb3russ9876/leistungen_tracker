# Lern-Tracker

Eine Python-Anwendung mit Streamlit, um Lernzeiten und Prüfungsnoten zu erfassen, auszuwerten und eine experimentelle Notenvorhersage zu erstellen.

Das Mini-Projekt verbindet Dateiverarbeitung, Datenanalyse, Visualisierung und erste Schritte mit Machine Learning.

## Funktionen

- Prüfungsdatum, Fach, Lernzeit in Stunden und Note erfassen.
- Einträge lokal in einer CSV-Datei speichern.
- Durchschnittliche Lernzeit und Durchschnittsnote pro Fach anzeigen.
- Die zeitliche Notenentwicklung für ein ausgewähltes Fach darstellen.
- Ab 20 Einträgen eine lineare Regression trainieren und mit MAE und R2 bewerten.
- Eine Note anhand von Lernzeit und Fach vorhersagen.

## Technologien

| Technologie | Verwendung |
|---|---|
| Python | Programmlogik und Dateiverarbeitung |
| Streamlit | Benutzeroberfläche im Browser |
| Pandas | Datenaufbereitung, Gruppierung und One-Hot-Encoding |
| Matplotlib und Seaborn | Diagramme |
| scikit-learn | Lineare Regression und Modellbewertung |

## Projektstruktur

| Datei | Aufgabe |
|---|---|
| `web_app_tracker.py` | Benutzeroberfläche und Ablauf der Anwendung |
| `lern_tracker.py` | CSV-Speicherung und Diagramme |
| `regressionsmodell.py` | Encoding, Datenaufteilung, Training und Kennzahlen |
| `leistungen.csv` | Lokal gespeicherte Einträge: entsteht beim ersten Speichern |

Die Python-Dateien müssen diese Namen tragen und im gleichen Ordner liegen, damit die Imports funktionieren.

## Installation und Start

Voraussetzung ist eine lokale Python-Installation mit `pip`. Lade das Repository herunter oder klone es und öffne ein Terminal im Projektordner.

### 1. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
```

Aktivieren unter Windows in der Eingabeaufforderung:

```bat
.venv\Scripts\activate.bat
```

Aktivieren unter Linux oder macOS:

```bash
source .venv/bin/activate
```

Je nach Installation lautet der Python-Befehl unter Linux oder macOS `python3`.

### 2. Abhängigkeiten installieren

```bash
python -m pip install streamlit pandas matplotlib seaborn scikit-learn
```

### 3. Anwendung starten

```bash
python -m streamlit run web_app_tracker.py
```

Öffne die im Terminal angezeigte lokale Adresse im Browser.

## Bedienung

1. Datum, Fach, Lernzeit und Prüfungsnote eingeben.
2. Den Eintrag mit **"Lernzeit und Note speichern"** speichern.
3. Die Durchschnittswerte ansehen und ein Fach für die Notenentwicklung auswählen.
4. Sobald mindestens 20 Einträge vorhanden sind, erscheint das Regressionsmodell. Beim Erreichen der Grenze kann eine weitere Interaktion nötig sein.
5. Lernzeit und Fach auswählen und die Vorhersage auslösen.

Fachnamen werden in Kleinbuchstaben gespeichert, Leerzeichen am Anfang und Ende werden entfernt. Verwende trotzdem einheitliche Bezeichnungen, beispielsweise immer `mathe` statt abwechselnd `mathe` und `mathematik`. Das Fach sollte nicht leer bleiben.

Die CSV enthält die Spalten `Datum`, `Fach`, `Lernzeit` und `Note`. Datumswerte werden im Format `TT.MM.JJJJ` gespeichert.

## Regressionsmodell

Das Modell nutzt die Lernzeit und das Fach als Eingabemerkmale. Fachnamen werden über One-Hot-Encoding in numerische Spalten umgewandelt, ein Fach dient als Referenz.

80% der Einträge dienen zum Training, 20% zur Bewertung. `random_state=17` macht die Aufteilung bei unveränderten Daten reproduzierbar. Das Modell wird im entsprechenden App-Zweig mit den aktuellen Daten neu trainiert.

- **MAE:** Durchschnittliche absolute Abweichung zwischen vorhergesagten und tatsächlichen Noten. Ein MAE von 0.4 bedeutet eine durchschnittliche Abweichung von 0.4 Notenpunkten im Testsatz.
- **R2:** Bestimmtheitsmass. Ein Wert von 1 bedeutet eine perfekte Vorhersage im Testsatz, 0 entspricht hinsichtlich des quadratischen Fehlers einer Vorhersage mit dessen Mittelwert. Negative Werte sind möglich. R2 ist keine prozentuale Genauigkeit.

## Grenzen

Die Vorhersage ist ein Lernexperiment. 20 Einträge ergeben nur vier Testwerte und reichen nicht für eine belastbare Bewertung. Auch wenige Beispiele pro Fach können die Ergebnisse stark beeinflussen.

Das Modell berücksichtigt weder Vorwissen noch Prüfungsschwierigkeit oder Lernmethode. Ein Zusammenhang zwischen Lernzeit und Note beweist keine Ursache. Mehr Daten verbessern die Vorhersagen nicht automatisch, Qualität und Relevanz der Daten sind ebenfalls entscheidend.

Die Begrenzung auf 1 bis 6 betrifft nur die angezeigte Vorhersage. Sie verbessert das Modell nicht, die Kennzahlen werden anhand der unbegrenzten Vorhersagen berechnet.

Die Anwendung ist für die lokale Nutzung gedacht. Eine Anmeldung, Mehrbenutzerverwaltung sowie das Bearbeiten oder Löschen einzelner Einträge sind nicht implementiert. Fehlerhafte oder manuell veränderte CSV-Dateien können zu Fehlern führen.
