from lark import Lark, Transformer

# Mermaid-Grammatik definieren
grammar = """
    start: subgraph*

    subgraph: "subgraph" CNAME "[" WS? "]" WS? statement* "end"

    statement: edge | node

    edge: CNAME ("--" | "---") cardinality? CNAME ("{" CNAME "}")?
    node: CNAME "---" ("[" STRING "]" | "((" STRING "))")

    cardinality: "(" NUMBER? ("," | ",*") NUMBER? ")"

    STRING: /`?<ins>.*?<\/ins>`?/ | /[^"]+/
    CNAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMBER: /\d+/
    WS: /\s+/
    %ignore WS
"""

# Transformer zum Verarbeiten der Parse-Bäume
class MermaidTransformer(Transformer):
    def start(self, items):
        return {
            "subgraphs": items
        }

    def subgraph(self, items):
        name = items[0]
        statements = items[1:]
        return {
            "subgraph": name,
            "statements": statements
        }

    def edge(self, items):
        source = items[0]
        target = items[2]
        cardinality = items[1] if len(items) > 3 else None
        label = items[3] if len(items) > 4 else None
        return {
            "type": "edge",
            "source": source,
            "target": target,
            "cardinality": cardinality,
            "label": label
        }

    def node(self, items):
        source = items[0]
        target = items[1]
        return {
            "type": "node",
            "source": source,
            "target": target
        }

    def cardinality(self, items):
        return "(" + ",".join(items) + ")"

# Lark-Parser initialisieren
mermaid_parser = Lark(grammar, parser="lalr", transformer=MermaidTransformer())

# Beispiel-Mermaid-Code
mermaid_code = """mermaid
flowchart
    subgraph SG1 [ ]
        Produzent---P1(["`<ins>ProdId</ins>`"])
        Produzent---P2([Name])
        Produzent---P3(((Zertifikate)))
    end
    subgraph SG2 [ ]
        Bauteil---B1(["`<ins>Name</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        B3---B4([Länge])
        B3---B5([Breite])
        B3---B6([Höhe])
    end
    subgraph SG3 [ ]
        Produzent--(1,*)---herstellen{herstellen}
        herstellen--(1,1)---Bauteil 
        herstellen---H1([Jahr])
    end
    subgraph SG4 [ ]
        Bauteil--(0,*)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil
    end    
"""

# Parsen des Mermaid-Codes
parsed_data = mermaid_parser.parse(mermaid_code)

# Ergebnisse anzeigen
import pprint
pprint.pprint(parsed_data)
