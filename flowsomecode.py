import code2flow
import json
from graphviz import Source

# code2flow.code2flow(['idutc.py', 'texioty.py', 'kinvow.py', 'artay.py'], 'DOTflows/idutc_dot.dot', language="py")
code2flow.code2flow(['glyther.py', 'glyphinator.py', 'wordie.py', 'fotoes.py'], 'DOTflows/artay_dot.dot', language="py")

with open("DOTflows/idutc_dot.json", 'r') as f:
    parsed = json.load(f)
    print(json.dumps(parsed, indent=4))

graph = Source.from_file('DOTflows/artay_dot.dot')
graph.render('DOTflows/output_graph', format='png', cleanup=True)
graph.view()
