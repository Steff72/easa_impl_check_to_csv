# EASA Part-FCL → OM-D Mapping CLI

Dieses Python-Tool automatisiert die Zuordnung von EASA Part‑FCL‑Regularien (Annex I) zu den entsprechenden Abschnitten im Unternehmens-Handbuch (OM D Rev29).

## Projektstruktur

```
project_root/
├── Pipfile               # Pipenv-Konfiguration
├── .env.example          # Beispiel für Umgebungsvariablen
├── .gitignore            # Git-Ausnahmen
├── README.md             # Projektdokumentation
├── regulations/          # Enthält die EASA-XML-Datei
│   └── Easy Access Rules for Aircrew.xml
├── documents/            # Unternehmens-Handbuch (nur lokal, nicht im Repo)
│   └── OM D Rev29.pdf
├── results/              # Generierte CSV-Ausgabe (nicht versioniert)
├── src/                  # Quellcode
│   ├── main.py           # CLI-Einstiegspunkt
│   ├── parse_regulations.py
│   ├── parse_document.py
│   ├── vector_search.py
│   ├── semantic_match.py
│   └── export_results.py
└── tests/                # Unit-Tests mit pytest
    ├── test_parse_regulations.py
    ├── test_parse_document.py
    ├── test_export_results.py
    └── test_vector_search.py  
```

## Voraussetzungen

* Python 3.8+ installiert
* [Pipenv](https://pipenv.pypa.io/) für Environment-Management
* OpenAI-API‑Key

## Installation

```bash
# Pipenv-Environment anlegen und Abhängigkeiten installieren
pipenv install --dev
```

## Umgebungsvariablen (`.env`)

Erstelle im Projektstamm eine Datei `.env` mit folgenden Einträgen:

```
OPENAI_API_KEY=dein_api_key
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4.1-mini
SIMILARITY_THRESHOLD=0.7
MAX_CANDIDATES=50
```

## Unternehmens-Handbuch

Lege das PDF `OM D Rev29.pdf` in den Ordner `documents/`. Dieser Ordner ist in `.gitignore` ausgenommen und enthält vertrauliche Unterlagen.

## Nutzung

```bash
# Mit Pipenv in das Environment wechseln
pipenv shell

# Mapping ausführen (XML + PDF → results/part-fcl_to_omd_map.csv)
python src/main.py --regs regulations/Easy\ Access\ Rules\ for\ Aircrew.xml --doc documents/OM\ D\ Rev29.pdf
```

## Tests

Die Unit-Tests prüfen die Kernelemente (XML-Parser, PDF-Split, CSV-Export).

```bash
pipenv run pytest  
```

## Ergebnis

Die CSV-Datei im Ordner `results/` listet in jeder Zeile eine Regulation und alle bestätigten OM-D-Abschnitte:

```
Regulation;Dokumentreferenz
"AMC1 FCL.050 a) Recording of flight time";"OM-D (29) 3.10.4"
"AMC1 FCL.050 a) Recording of flight time";"OM-D (29) 7.1.12"
...
```

---

