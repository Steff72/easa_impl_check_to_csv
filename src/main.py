#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# .env **vor** allen weiteren Imports laden und Werte erzwingen
load_dotenv(override=True)

import sys
import click

from parse_regulations import parse_regulations
from parse_document import parse_document_sections
from vector_search import init_chroma, search_candidates
from semantic_match import validate_candidates
from export_results import export_to_csv

@click.command()
@click.option(
    '--regs',
    default='regulations/Easy Access Rules for Aircrew (Regulation (EU) No 11782011) — Revision from August 2023 (XML).xml',
    help='Pfad zur XML-Regulationsdatei'
)
@click.option(
    '--doc',
    default='documents',
    help='Pfad zu einem Ordner mit PDF-Dateien'
)
@click.option(
    '--out',
    default='results/part-fcl_to_om_map.csv',
    help='Pfad zur Ausgabe-CSV'
)
def main(regs, doc, out):
    """
    CLI-Tool: Mappt EASA Part-FCL Regulations auf OM Handbook Sections
    """
    threshold = float(os.getenv('SIMILARITY_THRESHOLD', 0.7))
    max_cand = int(os.getenv('MAX_CANDIDATES', 50))

    click.echo("🔍 Starte Mapping-Prozess…")

    # 1. Regulations aus XML extrahieren
    click.echo(f"📄 Lade Regulations aus: {regs}")
    regulations = parse_regulations(regs)
    click.echo(f"  → Gefundene Regulations: {len(regulations)}")
    if not regulations:
        click.echo(f"❌ Fehler: Keine Regulations aus Datei '{regs}' extrahiert. Bitte prüfen.", err=True)
        sys.exit(1)

    # 2. Sektionen aus PDF extrahieren
    sections = {}
    if os.path.isdir(doc):
        click.echo(f"📑 Lade Dokumente aus Ordner: {doc}")
        pdf_files = [os.path.join(doc, f) for f in os.listdir(doc) if f.lower().endswith('.pdf')]
        pdf_files.sort()
        for pdf_file in pdf_files:
            file_name = os.path.basename(pdf_file)
            click.echo(f"  ↪ Extrahiere Sections aus: {file_name}")
            doc_sections = parse_document_sections(pdf_file)
            click.echo(f"    → Gefundene Sections in {file_name}: {len(doc_sections)}")
            for sec_id, content in doc_sections.items():
                combined_id = f"{file_name} {sec_id}"
                sections[combined_id] = content
    else:
        click.echo(f"📑 Lade Dokument und extrahiere Sections aus: {doc}")
        file_name = os.path.basename(doc)
        doc_sections = parse_document_sections(doc)
        click.echo(f"  → Gefundene Sections: {len(doc_sections)}")
        for sec_id, content in doc_sections.items():
            combined_id = f"{file_name} {sec_id}"
            sections[combined_id] = content

    if not sections:
        click.echo(f"❌ Fehler: Keine Abschnitte aus '{doc}' extrahiert. Bitte prüfen.", err=True)
        sys.exit(1)
    click.echo(f"  → Gesamt gefundene Sections: {len(sections)}")

    # 3. Chroma DB initialisieren und indexieren
    click.echo("🗄 Initialisiere Vector Database (Chroma)…")
    chroma_collection = init_chroma(sections)
    click.echo("  → Chroma-Collection bereit")

    results = []
    for idx, reg in enumerate(regulations, start=1):
        click.echo(f"🔎 [{idx}/{len(regulations)}] Suche Kandidaten für Regulation {reg['id']}")
        candidates = search_candidates(chroma_collection, reg['full_text'], threshold, max_cand)
        click.echo(f"  → {len(candidates)} Kandidaten nach Vektor-Filter")

        # 5. LLM-Validierung
        click.echo("   🧠 Validierung via LLM…")
        valid_ids = validate_candidates(reg, candidates, sections)
        click.echo(f"   → {len(valid_ids)} validierte Sections")

        for sec_id in valid_ids:
            results.append({
                'regulation': f"{reg['id']} {reg['title']}",
                'section': sec_id
            })

    # 6. CSV-Ausgabe
    click.echo(f"💾 Schreibe Ergebnisse nach {out} …")
    export_results_count = export_to_csv(results, out)
    click.echo(f"✅ Mapping abgeschlossen: {len(results)} Zuordnungen gespeichert.")

if __name__ == '__main__':
    main()