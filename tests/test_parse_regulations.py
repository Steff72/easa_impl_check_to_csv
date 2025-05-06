import pytest
from src.parse_regulations import parse_regulations

def test_parse_regulations(tmp_path):
    # Minimal-XML mit einer FCL-Regel und einer irrelevanten Regel
    xml = tmp_path / 'test.xml'
    xml.write_text('''<?xml version="1.0"?>
<root>
  <topic source-title="AMC1 FCL.050 a) Recording of flight time">
    <text>a) For the purposes of record-keeping in the pilot logbook, the operator shall record flight time.</text>
  </topic>
  <topic source-title="NOTFCL.001 Irrelevant">
    <text>ignore this</text>
  </topic>
</root>
''')
    regs = parse_regulations(str(xml))
    assert isinstance(regs, list)
    assert len(regs) == 1
    reg = regs[0]
    assert reg['id'] == 'AMC1 FCL.050 a)'
    assert 'pilot logbook' in reg['full_text']