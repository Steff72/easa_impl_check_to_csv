import csv
import os
from collections import OrderedDict


def export_to_csv(results: list[dict], out_path: str) -> int:
    """
    Schreibt die Zuordnungen in eine CSV‑Datei.

    * Die Reihenfolge der Regulations bleibt erhalten (Einfügereihenfolge).
    * Innerhalb derselben Regulation werden die Dokumentreferenzen
      alphabetisch sortiert.
    * Doppelte Kombinationen aus (Regulation, Section) werden entfernt.

    Gibt die Anzahl der geschriebenen Zeilen zurück.
    """
    # Regulations in Einfügereihenfolge gruppieren
    grouped: OrderedDict[str, set[str]] = OrderedDict()
    for row in results:
        reg = row["regulation"]
        sec = row["section"]
        grouped.setdefault(reg, set()).add(sec)  # set entfernt Duplikate

    # Zeilen in gewünschter Reihenfolge zusammenstellen
    sorted_rows: list[dict] = []
    for reg, sections in grouped.items():
        for sec in sorted(sections):
            sorted_rows.append({"regulation": reg, "section": sec})

    # CSV schreiben
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["regulation", "section"])
        writer.writeheader()
        writer.writerows(sorted_rows)

    return len(sorted_rows)