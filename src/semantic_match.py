import openai
import os
import json
import textwrap

def validate_candidates(regulation, candidates, sections):
    """
    Validate the candidate section IDs with an LLM, returning only those
    sections that truly implement the regulation.
    """
    # API-Key setzen
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-4.1-mini")

    # Prompt zusammenbauen
    prompt = textwrap.dedent(f"""
        Hier ist der vollständige EASA-Regeltext:
        {regulation['full_text']}

        Folgende Dokumentabschnitte könnten die Umsetzung sein:
    """)
    for i, sec_id in enumerate(candidates, start=1):
        excerpt = sections.get(sec_id, "")[:200].replace('\n', ' ')
        prompt += f"{i}) {sec_id} – \"{excerpt}\"\n"
    prompt += "\nBitte antworte mit einer JSON-Liste der Abschnittsnummern, die wirklich die Anforderungen umsetzen. Z.B.: [\"3.10.4\", \"7.1.12\"]"

    # Chat-Completion über die neue API aufrufen
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Du bist ein präziser Assistent, der überprüft, ob ein Dokumentabschnitt eine EASA-Regulation implementiert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    # Antwort parsen
    text = response.choices[0].message.content
    try:
        confirmed = json.loads(text)
    except json.JSONDecodeError:
        confirmed = []

    # Nur gültige, vorgefilterte IDs zurückgeben
    return [sec for sec in confirmed if sec in candidates]