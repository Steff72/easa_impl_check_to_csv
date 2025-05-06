import csv
import pytest
from src.export_results import export_to_csv

def test_export_to_csv(tmp_path):
    results = [
        {'regulation': 'AMC1 FCL.050 a) Recording of flight time', 'section': 'OM-D (29) 3.10.4'},
        {'regulation': 'AMC1 FCL.055 Language proficiency', 'section': 'OM-D (29) 7.1.12'}
    ]
    out = tmp_path / 'out.csv'
    export_to_csv(results, str(out))
    with open(out, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)
    assert rows[0]['Regulation'] == results[0]['regulation']
    assert rows[1]['Dokumentreferenz'] == results[1]['section']