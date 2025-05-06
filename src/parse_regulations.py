import xml.etree.ElementTree as ET
import re

# Nur echte FCL-Einträge (z. B. „FCL.050“, nicht „NOTFCL.001“)
fcl_pattern = re.compile(r"\bFCL\.\d+")

def parse_regulations(xml_path):
    """
    Parse the EASA XML und extrahiere Annex I (Part-FCL) Regulations.
    Liefert eine Liste von Dicts: {'id': ..., 'title': ..., 'full_text': ...}
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    regulations = []
    for elem in root.iter():
        if elem.tag.endswith('topic'):
            source_title = elem.attrib.get('source-title', '')
            # Filter auf echte FCL-Nummern
            if not fcl_pattern.search(source_title):
                continue

            tokens = source_title.split()
            # Bestimme ID und Titel
            if len(tokens) >= 3 and tokens[2].endswith(')'):
                reg_id = " ".join(tokens[:3])
                reg_title = " ".join(tokens[3:])
            else:
                reg_id = " ".join(tokens[:2])
                reg_title = " ".join(tokens[2:])

            # Sammle den vollen Text
            texts = []
            for child in elem:
                if child.tag.endswith('text') and child.text:
                    texts.append(child.text.strip())
            full_text = " ".join(texts) if texts else reg_title

            regulations.append({
                "id": reg_id,
                "title": reg_title,
                "full_text": full_text
            })
    return regulations