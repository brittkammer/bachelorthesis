import re 
import networkx as nx 


def parse_mermaid_text(mermaid_text):
    #regex_muster_knoten = r"(\w+)---(\w+)\(\[(?:(?:`?<ins>(.*?)<\/ins>`?)|([^\]]*?))\]\)|\((\w+)---(\w+)\(\(\((.*?)\)\)\)" 
    regex_muster_knoten = [
        r"(\w+)---(\w+)\(\[\"`?<ins>(.*?)<\/ins>`?\"\]\)",  # Mit <ins>-Tags - Primärschlüssel
        r"(\w+)---(\w+)\(\[(.*?)\]\)",                     # Ohne Tags - normales Attribut
        r"(\w+)---(\w+)\(\(\((.*?)\)\)\)"                  # Verschachtelte Klammern - zusammengesetztes Attribut
    ]

    regex_muster_kanten = [
        r"(\w+)\{(\w+)\}--\((\d,\*|\d,\d|\*?,\d)\)---(\w+)", # Relationship{}--()---Entiät
        r"(\w+)--\((\d,\*|\d,\d|\*?,\d)\)---(\w+)\{(\w+)\}" # Entität--()---Relationship{}
    ]

    graph = nx.DiGraph()
    lines = mermaid_text.split("\n") 

    for line in lines: 
        # Hinzufügen der Knoten
        for muster in regex_muster_knoten:
            matches = re.findall(muster, line)
            for entitaet, attribut_id, attribut_name in matches:
                graph.add_node(entitaet, type="Entität")
                graph.add_node(attribut_id, type="Attribut", label=attribut_name)
                graph.add_edge(entitaet, attribut_id, Beziehung="hat Attribut")

        # Hinzufügen der Kanten
        matches = re.findall(regex_muster_kanten[0], line) 
        for relationship,relation_name, cardinalitaet, entitaet in matches: 
            graph.add_node(relationship, type="Relationship"),
            graph.add_edge(relationship, entitaet,Beziehung="Relationship-Entität", Kardinalität=cardinalitaet)
        matches = re.findall(regex_muster_kanten[1], line)
        for entitaet, cardinalitaet, relationship, relationship_name in matches: 
            graph.add_node(relationship, type="Relationship"),
            graph.add_edge(entitaet, relationship, Beziehung="Entität-Relationship", Kardinalität=cardinalitaet)
    return graph 
    
mermaid_text =  """mermaid
flowchart
        Produzent---P1(["`<ins>ProdId</ins>`"])
        Produzent---P2([Name])
        Produzent---P3(((Zertifikate)))
        Bauteil---B1(["`<ins>Name</ins>`"])
        Bauteil---B2([Gewicht])
        Bauteil---B3([Größe])
        B3---B4([Länge])
        B3---B5([Breite])
        B3---B6([Höhe])
        Produzent--(1,*)---herstellen{herstellen}
        herstellen{herstellen}--(1,1)---Bauteil 
        herstellen---H1([Jahr])
        Bauteil--(0,*)---bestehen_aus{bestehen_aus}
        bestehen_aus{bestehen_aus}--(0,*)---Bauteil 
"""

graph = parse_mermaid_text(mermaid_text)

print("Knoten:")
for node, data in graph.nodes(data=True):
    print(node, data)

print("\nKanten:")
for u, v, data in graph.edges(data=True):
    print(u, v, data)