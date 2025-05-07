# EASA Implementation Checker

Dieses Tool bildet EASA Part‑FCL‑Regelungen automatisch auf die entsprechenden Abschnitte (Sections) eines oder mehrerer Betriebshandbücher (OM‑D PDFs) ab. Es kombiniert Vektor‑Suche (ChromaDB) mit einer LLM‑Validierung, um echte Umsetzungspassagen präzise zu erkennen und als CSV zu exportieren.

---

## Ordnerstruktur

```
├── regulations/     # EASA‑XML‑Regelwerke
├── documents/       # Zu prüfende Handbücher (PDFs)
├── results/         # CSV‑Ausgaben
├── .chromadb/       # Automatisch erstellte Vektor‑Datenbank
└── src/             # Python‑Quellcode
```

> **Wichtig:** Legen Sie **alle** zu prüfenden Manuals (PDF‑Dateien) im Ordner `documents/` ab. Das Programm verarbeitet beim Aufruf standardmäßig den gesamten Ordner.

---

## Installation

```bash
# 1. Repository klonen
$ git clone <repo‑url>
$ cd easa‑impl‑checker

# 2. Abhängigkeiten mit Pipenv installieren
$ pipenv install --python 3.11

# 3. Shell öffnen
$ pipenv shell

# 4. Umgebungsvariablen anlegen (.env)
#  (mindestens OPENAI_API_KEY muss gesetzt sein!)
OPENAI_API_KEY=<Ihr‑OpenAI‑Key>
# optionale Feintuning‑Parameter
SIMILARITY_THRESHOLD=0.7
MAX_CANDIDATES=50
```

> **Hinweis:** Legen Sie Ihren **OpenAI‑API‑Key** in der Datei `.env` als `OPENAI_API_KEY=...` ab oder exportieren Sie ihn als Umgebungsvariable, bevor Sie das Tool starten.

---

## Ausführung

```bash
# Standardaufruf verarbeitet alle PDFs im Ordner `documents/`
$ python src/main.py 
```

---

## Funktionsweise (Kurzfassung)

1. **Regulations parsen** – XML wird in einzelne Regeltexte zerlegt.
2. **PDF‑Abschnitte extrahieren** – Jede PDF im Ordner `documents/` wird section‑weise eingelesen.
3. **Vektor‑Index** – Alle Sections werden in eine Chroma‑Collection eingebettet.
4. **Kandidatensuche** – Für jede Regulation werden per Ähnlichkeitsscore Top‑K‑Kandidaten geholt.
5. **LLM‑Validierung** – GPT‑Modell prüft, welche Kandidaten den Regeltext wirklich erfüllen.
6. **Export** – Das Mapping wird als CSV gespeichert (`regulation`, `section`). Die Section enthält **Dateiname + Abschnitts‑ID** (z. B. `EDW OM D Rev29.pdf 3.4.2`). Das CSV wird im Ordner `results` gespeichert.

---

## Vektor‑Datenbank zurücksetzen

Das Programm legt alle Embeddings im Ordner `.chromadb/` ab. Um den Index neu aufzubauen (z. B. nach Änderung der PDFs), löschen Sie einfach den gesamten Ordner:

```bash
$ rm -rf .chromadb/
```

Beim nächsten Start wird die Datenbank automatisch frisch generiert.

---

## Hinweise

* Das Tool nutzt OpenAI GPT (standardmäßig `gpt-4.1-mini`).
* Für große PDF‑Sammlungen kann der erste Lauf einige Minuten dauern (Embedding‑Berechnung).
* Sie können Schwellenwerte (`SIMILARITY_THRESHOLD`, `MAX_CANDIDATES`) in `.env` feinjustieren.

Viel Erfolg beim Automatisieren des Compliance‑Checks!
