import openai
import os
import json
import textwrap


def validate_candidates(regulation, candidates, sections):
    """
    Use GPT to validate each candidate section for the given regulation.
    Returns list of confirmed section IDs that implement the regulation.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-4.1-mini")
    prompt = textwrap.dedent(f"""\
    Hier ist der vollständige EASA-Regeltext:
    {regulation['full_text']}

    Folgende Dokumentabschnitte könnten die Umsetzung sein (Nummer und kurzer Auszug):
    """
    )
    for i, sec_id in enumerate(candidates, start=1):
        excerpt = sections.get(sec_id, "")[:200].replace('\n', ' ')
        prompt += f"{i}) {sec_id} – \"{excerpt}\"\n"
    prompt += textwrap.dedent("""
    Bitte antworte mit einer JSON-Liste der Abschnittsnummern, die die Anforderungen dieser Regulation tatsächlich umsetzen. Zum Beispiel:
    ["3.10.4", "7.1.12"]
    """)
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Du bist ein präziser Assistent, der überprüft, ob ein Dokumentabschnitt eine gegebene EASA-Regulation implementiert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    content = response.choices[0].message.content.strip()
    try:
        confirmed = json.loads(content)
    except json.JSONDecodeError:
        confirmed = []
    return [sec for sec in confirmed if sec in candidates]