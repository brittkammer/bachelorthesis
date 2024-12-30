from lark import Lark

grammar = """
    start: entitaet+ relationship*

    entitaet: NAME "(" attribute ("," attribute)* ")"
    attribute: "*" NAME | "[" NAME "]" | NAME
    relationship: NAME "--" cardinalitaet "--" NAME "--" cardinalitaet "--" NAME
    cardinalitaet: "(" NUMBER "," NUMBER ")"
    
    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar)

# Beispiel für Parsing
input_text = """
Produzent (*ProdId, Name, [Zertifikate])
Bauteil (*Name, Gewicht, Größe(Länge, Breite, Höhe))
Produzent -- (1,*) -- herstellen (Jahr) -- (1,1) -- Bauteil
"""
tree = parser.parse(input_text)
print(tree.pretty())