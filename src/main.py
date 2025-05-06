#!/usr/bin/env python3
import os
import click
from dotenv import load_dotenv
from parse_regulations import parse_regulations
from parse_document import parse_document_sections
from vector_search import init_chroma, search_candidates
from semantic_match import validate_candidates
from export_results import export_to_csv

@click.command()
@click.option('--regs', default='regulations/Easy Access Rules for Aircrew.xml', help='Pfad zur XML-Regulationsdatei')
@click.option('--doc', default='documents/OM D Rev29.pdf', help='Pfad zur OM-D PDF-Datei')
@click.option('--out', default='results/part-fcl_to_omd_map.csv', help='Pfad zur Ausgabe-CSV')
def main(regs, doc, out):
    """
    CLI-Tool: Mappt EASA Part-FCL Regulations auf OM-D Handbook Sections
    """
    load_dotenv()
    threshold = float(os.getenv('SIMILARITY_THRESHOLD', 0.7))
    max_cand = int(os.getenv('MAX_CANDIDATES', 50))

    # 1. Regulations aus XML extrahieren
    regulations = parse_regulations(regs)
    # 2. Sektionen aus PDF extrahieren
    sections = parse_document_sections(doc)
    # 3. Chroma DB initialisieren und indexieren
    chroma_client = init_chroma(sections)

    results = []
    for reg in regulations:
        # 4. Vorfiltern via Vektorensuche
        candidates = search_candidates(chroma_client, reg['full_text'], threshold, max_cand)
        # 5. LLM-Validierung
        valid_ids = validate_candidates(reg, candidates, sections)
        for sec_id in valid_ids:
            results.append({
                'regulation': f"{reg['id']} {reg['title']}",
                'section': f"OM-D (29) {sec_id}"
            })
    # 6. CSV-Ausgabe
    export_to_csv(results, out)

if __name__ == '__main__':
    main()